from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import os
import logging
import json
from function_extractor import get_function_names
from core import Generator
import base64

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:9013"}}, supports_credentials=True)


@app.route('/upload-files', methods=['PUT'])
def save_business_code():
    cookie = request.cookies.get('session_id')

    file = request.files.get('file')
    folder = os.path.join('temp', cookie)
    Path(folder).mkdir(parents=True, exist_ok=True)
    file.save(os.path.join(folder, file.filename))

    return jsonify(get_function_names(os.path.join(folder, file.filename)))


@app.route('/generate', methods=['PUT'])
def generate():
    cookie = request.cookies.get('session_id')

    bpmn = request.form.get('bpmn')
    endpoints = request.form.get('endpoints')

    folder = os.path.join('temp', cookie)
    with open(os.path.join(folder, 'diagram.bpmn'), "w") as text_file:
        text_file.write(bpmn)

    endpoints = json.loads(endpoints)

    generator = Generator(endpoints['provider'])
    deployment_package_path = generator.generate(folder, endpoints['endpoints'])

    with open(deployment_package_path, mode="rb") as binary_file:
        binary_file = binary_file.read()
        binary_file = base64.b64encode(binary_file)
        binary_file = binary_file.decode('utf-8')

    _, filename = os.path.split(deployment_package_path)

    return json.dumps({'filename': filename, 'file': binary_file})


if __name__ == '__main__':
    app.run()
