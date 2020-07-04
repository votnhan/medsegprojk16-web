from flask import Blueprint, request, jsonify, session

api_hp = Blueprint('api_hp', 'api_hp', url_prefix='/api-hp')

@api_hp.route('/')
def get_hp():
    return 'Welcome to homepage !'