<<<<<<< HEAD
import ast
from exec import find_exec_usage
from shell_injection import find_shell_issues, has_shell, _evaluate_shell_call
from yaml_load import find_yaml_load_usage
from eval import find_eval_usage
from try_except_continue import try_except_continue_code
from try_except_pass import try_except_pass_code
from wildcard_injection import find_wildcard_injection_issues
from hardcoded_password import analyze_code

def main():
    code_path = input("Enter the path to the Python code file: ")
    
    try:
        with open(code_path, "r") as file:
            python_code = file.read()
            tree = ast.parse(python_code)
            
            # Exec Checker
            exec_issues = find_exec_usage(tree)

            if exec_issues:
                print("\nexec() Usage Issues:")
=======


import ast
from exec import find_exec_usage
from shell_injection import find_shell_issues, has_shell, _evaluate_shell_call
from yalm import find_yaml_load_usage, _check_yaml_load


def main():
    code_path = input("Enter the path to the Python code file: ")
    try:
        with open(code_path, "r") as file:
            python_code = file.read()

            # Exec Checker
            exec_tree = ast.parse(python_code)
            exec_issues = find_exec_usage(exec_tree)

            if exec_issues:
                print("\nExec Usage Issues:")
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
                for issue in exec_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No exec usage issues found in the provided code.")

<<<<<<< HEAD
            # Eval Checker
            eval_issues = find_eval_usage(tree)

            if eval_issues:
                print("\neval() Usage Issues:")
                for issue in eval_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No eval usage issues found in the provided code.")

            # Shell Checker
            shell_issues = find_shell_issues(tree)
=======
            # Shell Checker
            shell_tree = ast.parse(python_code)
            config = {
                "subprocess": [
                    "subprocess.Popen",
                    "subprocess.call",
                    "subprocess.check_call",
                    "subprocess.check_output",
                    "subprocess.run",
                ],
                "shell": [
                    "os.system",
                    "os.popen",
                    "os.popen2",
                    "os.popen3",
                    "os.popen4",
                    "popen2.popen2",
                    "popen2.popen3",
                    "popen2.popen4",
                    "popen2.Popen3",
                    "popen2.Popen4",
                    "commands.getoutput",
                    "commands.getstatusoutput",
                ],
            }
            shell_issues = find_shell_issues(shell_tree, config)
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4

            if shell_issues:
                print("\nShell Injection Issues:")
                for issue in shell_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No Shell Injection issues found in the provided code.")

            # YAML Checker
<<<<<<< HEAD
            yaml_issues = find_yaml_load_usage(tree)
=======
            yaml_tree = ast.parse(python_code)
            yaml_issues = find_yaml_load_usage(yaml_tree)
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4

            if yaml_issues:
                print("\nYAML Load Usage Issues:")
                for issue in yaml_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No YAML load usage issues found in the provided code.")

<<<<<<< HEAD

            # Try Except Continue Checker
            try_except_continue_issues = try_except_continue_code(tree)

            if try_except_continue_issues:
                print("\nTry Except Continue Issues:")
                for issue in try_except_continue_issues:
                    print(f"Line {issue['line']}: {issue['text']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})")
            else:
                print("No Try Except Continue usage issues found in the provided code.")
            
            
            # Try Except Pass Checker
            try_except_pass_issues = try_except_pass_code(tree)

            if try_except_pass_issues:
                print("\nTry Except Pass Issues:")
                for issue in try_except_pass_issues:
                    print(f"Line {issue['line']}: {issue['text']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})")
            else:
                print("No Try Except Pass usage issues found in the provided code.")
                   
            #Wildcard Injection
            wildcard_injection_issues = find_wildcard_injection_issues(tree)
            
            if wildcard_injection_issues:
                for issue in wildcard_injection_issues:
                    print(f"Line {issue['line']}: {issue['text']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})")
            else:
                print("No Wildcard Injection issues found in the provided code.")
                
                
            
            #Hardcoded Password
            hardcoded_password_issues = analyze_code(tree)
            
            if hardcoded_password_issues:
                for issue in hardcoded_password_issues:
                    print(f"{issue['location']}: {issue['text']} (Severity: {issue['severity']}, Confidence: {issue['confidence']}, CWE: {issue['cwe']})")

            else:
                print("No Hardcoded Password issues found in the provided code.")

    

=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
    except FileNotFoundError:
        print(f"File not found: {code_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

