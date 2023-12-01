import os
import sys
import json
from CFGhelper import CFGCreator  # Assuming CFG_helper.py is correctly placed
from ASTParser import parse_python_file, ast_to_dict
from ASTencoder import rename

def ensure_database_directory():
    database_dir = os.path.join(os.path.dirname(__file__), '..', 'Database')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    return database_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python __main__.py <Python file>")
        sys.exit(1)

    input_file = sys.argv[1]
    database_dir = ensure_database_directory()

    # Parse the Python file to AST using ASTParser.py
    ast_tree = parse_python_file(input_file)

    # Save AST to JSON
    ast_json_path = os.path.join(database_dir, 'ast.json')
    with open(ast_json_path, 'w') as file:
        json.dump(ast_to_dict(ast_tree), file, indent=4)
    
    rename()

    # Create CFG from AST and save as JSON
    cfg_creator = CFGCreator()
    cfg_creator.visit(ast_tree)
    cfg_json_path = os.path.join(database_dir, 'cfg.json')
    with open(cfg_json_path, 'w') as file:
        # Implement the logic to convert CFG to a serializable format if necessary
        # json.dump(cfg_serializable, file, indent=4)
        print(f"AST and CFG for {input_file} have been saved in {database_dir}")

if __name__ == "__main__":
    main()

