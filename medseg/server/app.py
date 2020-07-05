# for demo with colab
# from flask_ngrok import run_with_ngrok

from dotenv import load_dotenv
load_dotenv('env.txt')

from flask import Flask
from blueprint.homepage import api_hp
from blueprint.file_handler import api_file
from blueprint.prediction import api_pred


app = Flask(__name__)

# for demo with colab
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)

app.register_blueprint(api_hp)
app.register_blueprint(api_file)
app.register_blueprint(api_pred)

@app.route('/')
def main():
    return 'Welcome !'

if __name__ == '__main__':
    app.run()