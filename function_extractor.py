import ast
import os
import shutil
import json
from pathlib import Path
from zipfile import ZipFile


def __get_function(function_node) -> dict:
    function = {'function': function_node.name}
    #print("\tFunction name:", function_node.name)
    #print("\tArgs:")
    args = function_node.args.args
    function['args'] = []
    for arg in args:
        #print("\t\tParameter name:", arg.arg)
        function['args'].append(arg.arg)
    return function


def __get_modules(handler_path) -> list:
    counter: int = 0
    modules = []

    for filename in os.listdir(handler_path):
        if filename.endswith('.py'):
            with open(os.path.join(handler_path, filename)) as file:
                node = ast.parse(file.read())

            #print()
            #print('Module:', filename)
            modules.append({'module': filename, 'functions': []})

            functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]

            for function in functions:
                modules[counter]['functions'].append(__get_function(function))

            counter += 1

    return modules


def __empty_temp_folder():
    folder: str = 'temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_function_names(zip_path) -> json:
    zip_filename: str = Path(zip_path).stem
    ZipFile(zip_path, 'r').extractall(os.path.dirname(zip_path))
    os.rename(zip_path, zip_path+'.input')

    folder: str = os.path.join(os.path.dirname(zip_path), zip_filename)

    result = {'project': zip_filename, 'modules': __get_modules(folder)}

    #__empty_temp_folder()
    return json.dumps(result)
