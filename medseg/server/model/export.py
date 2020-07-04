import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from imageio import mimwrite
from .predict import generate_predition_case

ext_gif = '.gif'
ext_mri= '.nii.gz'
fps = 15
rgb_range = (0, 255)
red, green, blue = (255, 0, 0), (0, 0, 255), (0, 255, 0)


def create_modal_with_mask_np(subject_fd, modal_file, mask_file):
    md_tf = create_modal_ts(subject_fd, modal_file)
    
    label_path = os.path.join(subject_fd, mask_file)
    l = nib.load(label_path)
    label = l.get_data()

    label = np.rollaxis(label, 2, 0)
    d = label.shape[0]
    label = [np.rot90(label[i, :, :].T, k=2) for i in range(d)]
    label = np.asarray(label)

    ed = label == 2
    eh = label == 4
    neh = label == 1

    md_tf[ed] = red
    md_tf[eh] = green
    md_tf[neh] = blue
    
    return md_tf

def create_modal_ts(subject_fd, modal_file):
    modal_path = os.path.join(subject_fd, modal_file)
    d = nib.load(modal_path)
    md_data = d.get_data()

    min_val = np.min(md_data)
    max_val = np.max(md_data)
    md_data = ((md_data - min_val)*rgb_range[1]/(max_val - min_val) + rgb_range[0]).astype(np.uint8)

    depth = md_data.shape[2]
    md_tf = [ np.flip(md_data[:, :, i]).T for i in range(depth) ]
    md_tf = np.asarray(md_tf)
    md_tf = np.expand_dims(md_tf, axis=3)
    md_tf = np.tile(md_tf, (1, 1, 1, 3))
    return md_tf

def gif_export_subject(subject_fd, modal_type, key, output_fd, model):
    modal_file = modal_type + ext_mri
    mask_file = key + ext_mri
    mask_file_path = os.path.join(subject_fd, mask_file)
    
    if not os.path.exists(mask_file_path):
        generate_predition_case(subject_fd, subject_fd, key, model)

    output_file_path = os.path.join(output_fd, key + '_' + modal_type + '_masked' + ext_gif)
    
    if not os.path.exists(output_file_path):
        md_tf = create_modal_ts(subject_fd, modal_file)
        md_tf_masked = create_modal_with_mask_np(subject_fd, modal_file, mask_file)
        combination = np.concatenate((md_tf, md_tf_masked), axis=2)
        mimwrite(output_file_path, combination, format='gif', fps=fps)
    
    return output_file_path

def gif_export_subject_with_label(subject_fd, modal_file, truth_file, predicted_file, output_fd):
    md_tf_truth = create_modal_with_mask_np(subject_fd, modal_file, truth_file)
    md_tf_pred = create_modal_with_mask_np(subject_fd, modal_file, predicted_file)
    combined_tf = np.concatenate((md_tf_truth, md_tf_pred), axis=2)
    output_file_path = os.path.join(output_fd, modal_file+'_combine_pred'+ext_gif)
    mimwrite(output_file_path, combined_tf, format='gif', fps=fps)
    return output_file_path

def gif_export_modal(subject_fd, modal_type, key, output_fd):
    modal_file = modal_type + ext_mri
    output_file_path = os.path.join(subject_fd, key + '_' + modal_type + ext_gif)

    if not os.path.exists(output_file_path):
        md_tf = create_modal_ts(subject_fd, modal_file)
        mimwrite(output_file_path, md_tf, format='gif', fps=fps)

    return output_file_path