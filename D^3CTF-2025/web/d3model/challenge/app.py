import keras
from flask import Flask, request, jsonify
import os


def is_valid_model(modelname):
    try:
        keras.models.load_model(modelname)
    except:
        return False
    return True

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return open('index.html').read()


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds 50MB limit'}), 400
    
    filepath = os.path.join('./', 'test.keras')
    if os.path.exists(filepath):
        os.remove(filepath)
    file.save(filepath)
    
    if is_valid_model(filepath):
        return jsonify({'message': 'Model is valid'}), 200
    else:
        return jsonify({'error': 'Invalid model file'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
