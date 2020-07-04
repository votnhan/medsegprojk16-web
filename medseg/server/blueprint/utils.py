import os, zipfile
from ast import literal_eval

all_modalities = literal_eval(os.getenv('all_modalities'))
ext_mri = os.getenv('ext_mri')

def create_subject_folder(output_path, input_file, hashkey):
    path_to_zip_file = os.path.join(output_path, input_file)
    hashed_folder = os.path.join(output_path, hashkey)
    os.mkdir(hashed_folder)
    
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(hashed_folder)

    return hashed_folder, path_to_zip_file

def check_key_existence(key):
    file_ct = os.getenv('file_container_path')
    keys = os.listdir(file_ct)
    return key in keys

def validate_modality(hashed_folder):
    t = os.listdir(hashed_folder)[0]
    subject_fd = os.path.join(hashed_folder, t)
    l = os.listdir(subject_fd)
    modal_files = [x + ext_mri for x in all_modalities]
    result = []

    for x in  modal_files:
        if not x in l:
            result.append(x)

    return result