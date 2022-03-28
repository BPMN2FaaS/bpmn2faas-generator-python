import flask
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
import os
import logging
import json
from function_extractor import get_function_names
from core import Generator

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:9013"}}, supports_credentials=True)


@app.route('/upload-files', methods=['PUT'])
def save_business_code():
    cookie = request.cookies.get('session_id')
    print(cookie)

    file = request.files.get('file')
    folder = os.path.join('temp', cookie)
    Path(folder).mkdir(parents=True, exist_ok=True)
    file.save(os.path.join(folder, file.filename))

    return jsonify(get_function_names(os.path.join(folder, file.filename)))

@app.route('/generate', methods=['PUT'])
def generate():
    cookie = request.cookies.get('session_id')
    print(cookie)

    bpmn = request.form.get('bpmn')
    endpoints = request.form.get('endpoints')

    folder = os.path.join('temp', cookie)
    with open(os.path.join(folder, 'diagram.bpmn'), "w") as text_file:
        text_file.write(bpmn)
    with open(os.path.join(folder, 'endpoints.json'), "w") as text_file:
        text_file.write(endpoints)

    generator = Generator('test')

    return 'hello'


if __name__ == '__main__':
    app.run()
