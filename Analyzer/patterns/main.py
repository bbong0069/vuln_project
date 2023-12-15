import ast
from exec import find_exec_usage
from shell_injection import find_shell_issues, has_shell, _evaluate_shell_call
from yaml_load import find_yaml_load_usage
from eval import find_eval_usage
from try_except_continue import try_except_continue_code
from try_except_pass import try_except_pass_code
from wildcard_injection import find_wildcard_injection_issues
from hardcoded_password import hardcoded_password_usage
from pickle import pickle_usage
def main():
    code_path = input("Enter the path to the Python code file: ")
    
    try:
        with open(code_path, "r") as file:
            python_code = file.read()
            tree = ast.parse(python_code) #입력받은 코드로 AST트리 생성
            
            # Exec Checker
            exec_issues = find_exec_usage(tree)

            if exec_issues:
                print("\nexec() Usage Issues:")
                for issue in exec_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No exec usage issues found in the provided code.")

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

            if shell_issues:
                print("\nShell Injection Issues:")
                for issue in shell_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No Shell Injection issues found in the provided code.")

            # YAML Checker
            yaml_issues = find_yaml_load_usage(tree)

            if yaml_issues:
                print("\nYAML Load Usage Issues:")
                for issue in yaml_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No YAML load usage issues found in the provided code.")


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
            hardcoded_password_issues = hardcoded_password_usage(tree)
            
            if hardcoded_password_issues:
                for issue in hardcoded_password_issues:
                    print(f"{issue['location']}: {issue['text']} (Severity: {issue['severity']}, Confidence: {issue['confidence']}, CWE: {issue['cwe']})")

            else:
                print("No Hardcoded Password issues found in the provided code.")

            
            pickle_issues = pickle_usage(tree)
            
            if pickle_issues:
            	for issue in pickle_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})")
            else:
                print("No pickle issues found in the provided code.")
            

    except FileNotFoundError:
        print(f"File not found: {code_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
