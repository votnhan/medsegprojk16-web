import os
from flask import Blueprint, request, session, jsonify, send_file
from model.unet3d.training import load_old_model
from model.predict import generate_predition_case
from model.export import gif_export_subject
from .utils import check_key_existence

import tensorflow as tf
import keras.backend.tensorflow_backend as tfback

def _get_available_gpus():
    """Get a list of available gpu devices (formatted as strings).

    # Returns
        A list of available GPU devices.
    """
    #global _LOCAL_DEVICES
    if tfback._LOCAL_DEVICES is None:
        devices = tf.config.list_logical_devices()
        tfback._LOCAL_DEVICES = [x.name for x in devices]
    return [x for x in tfback._LOCAL_DEVICES if 'device:gpu' in x.lower()]

tfback._get_available_gpus = _get_available_gpus

api_pred = Blueprint('api_pred', 'api_pred', url_prefix='/api-pred')

model_file_path = os.path.join(os.getenv('model_fd'), os.getenv('model_filename'))
model = load_old_model(model_file_path)
model._make_predict_function()

@api_pred.route('/getmask', methods=['POST'])
def get_mask():
    key = request.form.get('key')
    if key:
        if not check_key_existence(key):
            return jsonify(status=404, message='Key not found')
        
        subject_fd = get_subject_fd(key)
        output_path = generate_predition_case(subject_fd, subject_fd, key, model)
        return send_file(output_path, as_attachment=True)
    else:
        return jsonify(status=400, message='Payload key not found')

@api_pred.route('/getgif', methods=['POST'])
def get_gif():
    key = request.form.get('key')
    modal_type = request.form.get('modal_type')
    
    if not key:
        return jsonify(status=400, message='Payload key not found')

    elif not modal_type:
        return jsonify(status=400, message='Modal type not found')
        
    if not check_key_existence(key):
        return jsonify(status=404, message='Key not found')
        
    subject_fd = get_subject_fd(key)
    output_path = gif_export_subject(subject_fd, modal_type, key, subject_fd, model)
    return send_file(output_path, as_attachment=True)


def get_subject_fd(key):
    subject_fd = os.path.join(os.getenv('file_container_path'), key)
    t = os.listdir(subject_fd)[0]
    subject_fd = os.path.join(subject_fd, t)
    return subject_fd