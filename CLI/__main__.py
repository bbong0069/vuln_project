import sys
import astor
from CFGhelper import CFGCreator  # Assuming CFG_helper.py is correctly placed
from ASTParser import *
from ASTencoder import *
from ..Config.FilePathManager import *
from staticfg_link import *

import RenameVariables



def main():
    if len(sys.argv) < 2:
        print("Usage: python __main__.py <Python file>")
        sys.exit(1)

    FilePathManger = FilePathManager(sys.argv[1])
    database_dir = ensure_database_directory()

    # Parse the Python file to AST using ASTParser.py and save ast
    ast_tree = parse_python_file(FilePathManger.code_path)
    FilePathManger.save_ast(FilePathManger.ast_path, ast_to_dict(ast_tree))


    # update FilePathManager.py
    '''    
    # Save AST to JSON
    ast_json_path = os.path.join(database_dir, 'ast.json')
    with open(ast_json_path, 'w') as file:
        json.dump(ast_to_dict(ast_tree), file, indent=4)
    '''

    # RenameVariables code
    after_change = change_name(ast_tree)
    FilePathManger.write_modified_code(after_change)

    run_cfg()
    '''
        # Create CFG from AST and save as JSON
        cfg_creator = CFGCreator()
        cfg_creator.visit(ast_tree)
        # Implement the logic to convert CFG to a serializable format if necessary
        # json.dump(cfg_serializable, file, indent=4)
        FilePathManger.save_ast(FilePathManger.cfg_path, cfg_serializable)
        print(f"AST and CFG for {FilePathManger.code_path} have been saved in {FilePathManger.database_dir}")
    '''

def change_name(ast):
    RenameVariables().visit(ast)
    new_code = astor.to_source(ast)
    return new_code


if __name__ == "__main__":
    main()

