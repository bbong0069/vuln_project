import json
import os

class FilePathManager:
    def __init__(self, code_path, modified_path='modified_code.py', ast_path='ast.json', cfg_path='cfg.json'):
        
        file_path = ensure_database_directory()

        self.code_path = code_path
        self.modified_path = file_path + modified_path
        self.ast_path = file_path + ast_path
        self.cfg_path = file_path + cfg_path

    def read_code(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_code(self, path, code):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(code)

    def read_code(self):
        return self.read_code(self.code_path)

    def write_modified_code(self, code):
        self.write_code(self.modified_path, code)

    def save_ast(self, path, tree):
        with open(path, 'w') as file:
            json.dump(tree, file, indent=4)


def ensure_database_directory():
    database_dir = os.path.join(os.path.dirname(__file__), '..', 'Database')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    return database_dir