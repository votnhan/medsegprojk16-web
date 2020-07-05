import os
import nibabel as nib
import numpy as np
import copy
from .unet3d.utils.utils import resize, read_image, crop_img_to, fix_shape
from .unet3d.prediction import prediction_to_image
from ast import literal_eval

means = [1002.8655, 754.4905, 185.99873, 260.69287]
stds = [1173.731, 882.37555, 228.1578, 323.1486]

all_modalities = literal_eval(os.getenv('all_modalities'))
ext_mri = os.getenv('ext_mri')
original_shape = (240, 240, 155)
input_shape = (128, 128, 128)
labels = (0, 1, 2, 4)
background_value = 0
tolerance = 0.00001
rtol = 1e-8

def crop_subject_modals(subject_modal_imgs, input_shape, slices):
    subject_data = []
    affine = None
    for i, modal_img in enumerate(subject_modal_imgs):
        modal_img = fix_shape(modal_img)
        modal_img = crop_img_to(modal_img, slices, copy=True)
        new_img = resize(modal_img, new_shape=input_shape, interpolation='linear')
        subject_data.append(new_img.get_data())
        if i == 0:
            affine = new_img.get_affine()
    
    subject_data = np.asarray(subject_data)
    return subject_data, affine

def get_subject_tensor(subject_folder):
    input_mris = []
    affine = None
    for i, modal in enumerate(all_modalities):
        path_modal = os.path.join(subject_folder, modal + ext_mri)
        modal_image = nib.load(path_modal)
        modal_tensor = modal_image.get_data()
        is_foreground = np.logical_or(modal_tensor < (background_value - tolerance),
                                      modal_tensor > (background_value + tolerance))
        
        if i == 0:
          foreground = np.zeros(is_foreground.shape, dtype=np.uint8)
          affine = modal_image.get_affine()

        input_mris.append(modal_image)
        foreground[is_foreground] = 1

    return input_mris, affine, foreground

def normalize_data(input_tensor):
    input_tensor = input_tensor.astype(np.float32)
    brain_mask = [input_tensor[i] > 0 for i in range(input_tensor.shape[0])]
    brain_data = [input_tensor[i][mask] for i, mask in enumerate(brain_mask)]
    
    means = np.asarray([x.mean() for x in brain_data])
    stds = np.asarray([x.std() for x in brain_data])

    result = copy.deepcopy(input_tensor)
    for i, mask in enumerate(brain_mask):
      result[i][mask] = (input_tensor[i][mask] - means[i]) / stds[i]

    return result

def predict(model, image_tensor, affine):
    import keras.backend.tensorflow_backend as tfb
    tfb._SYMBOLIC_SCOPE.value = True
    result = model.predict(image_tensor)
    image_label = prediction_to_image(result, affine, label_map=True, labels=labels)
    return image_label

def restore_dimension(image_label, slices, affine):
    old_shape = tuple([x.stop - x.start for x in slices])
    old_cropped_image = resize(image_label, old_shape, interpolation='nearest')
    rotated_image = np.rot90(old_cropped_image.get_data(), 2)
    result = np.zeros(original_shape, dtype=np.uint8)
    tp_slices = tuple(slices)
    result[tp_slices] = rotated_image
    return nib.Nifti1Image(result, affine)

def get_slices(foreground):
    infinity_norm = max(-np.min(foreground), np.max(foreground))
    passes_threshold = np.logical_or(foreground < -rtol * infinity_norm,
                            foreground > rtol * infinity_norm)
    coords = np.array(np.where(passes_threshold))
    start = coords.min(axis=1)
    end = coords.max(axis=1) + 1
    start = np.maximum(start - 1, 0)
    end = np.minimum(end + 1, foreground.shape[:3])
    slices = [slice(s, e) for s, e in zip(start, end)]
    return slices

def create_prediction_ts(subject_fd, model):
    image_mris, original_affine, foreground = get_subject_tensor(subject_fd)
    slices = get_slices(foreground)
    subject_data_fixed_size, affine = crop_subject_modals(image_mris, input_shape, slices)
    subject_tensor = normalize_data(subject_data_fixed_size)
    subject_tensor = np.expand_dims(subject_tensor, axis=0)
    output_predict = predict(model, subject_tensor, affine)
    output = restore_dimension(output_predict, slices, original_affine)
    return output

def generate_predition_case(subject_fd, output_fd, key, model):
    output_file = os.path.join(output_fd, key + ext_mri)
    
    if not os.path.exists(output_file):
        output = create_prediction_ts(subject_fd, model)
        output.to_filename(output_file)
    
    return output_file