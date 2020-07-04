import os, uuid, shutil
from flask import Blueprint, request, jsonify, session, send_file
from .utils import create_subject_folder, validate_modality

api_file = Blueprint('api_file', 'api_file', url_prefix='/api-file')
file_container_path = os.getenv('file_container_path')
zipets = os.getenv('ext_zip')

@api_file.route('/sendfile', methods=['POST'])
def handle_sending_file():
    if 'file' not in request.files:
        return jsonify(status=400, message='No file part')
    
    filesend = request.files['file']
    if filesend.filename == '':
        return jsonify(status=400, message='No selected file')

    hashkey = uuid.uuid4().hex
    filesend.save(os.path.join(file_container_path, hashkey + zipets))
    hashed_folder, path_zip_file = create_subject_folder(file_container_path, hashkey + zipets, hashkey)
    modal_shortage = validate_modality(hashed_folder)
   
    if modal_shortage != []:
        os.remove(path_zip_file)
        shutil.rmtree(hashed_folder)
        return jsonify(status=400, message='Modality stortage', shortage=str(modal_shortage))

    return  jsonify(status=200, message='Send successfully', key=hashkey)

# @api_file.route('/getfilemask', methods=['GET'])
# def get_file():
#     filename = 'Brats18_MDA_907_1_t1.nii.gz'
#     c = 'Brats18_MDA_907_1'
#     key = '6a038cbe82604b67bd5d14ddceaf5278'
#     output_path = os.path.join(file_container_path, key, c, filename)
#     return send_file(output_path, as_attachment=True)
