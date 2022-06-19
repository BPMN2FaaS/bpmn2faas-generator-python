[![PyPI pyversions](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)

# BPMN2FaaS Generator (Python)

## How to run

Install all required dependencies:

```
pip install -r requirements.txt
```
Install plugins (aws/azure):

```
cd plugins
git clone https://github.com/BPMN2FaaS/bpmn2faas_{aws|azure}_plugin_python.git
cd bpmn2faas_{aws|azure}_plugin_python
pip install -r requirements.txt
cd ../..
```
Run Generator:

```
python -m flask run --port 8001
```
