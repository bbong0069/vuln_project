

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
                for issue in exec_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No exec usage issues found in the provided code.")

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

            if shell_issues:
                print("\nShell Injection Issues:")
                for issue in shell_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No Shell Injection issues found in the provided code.")

            # YAML Checker
            yaml_tree = ast.parse(python_code)
            yaml_issues = find_yaml_load_usage(yaml_tree)

            if yaml_issues:
                print("\nYAML Load Usage Issues:")
                for issue in yaml_issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No YAML load usage issues found in the provided code.")

    except FileNotFoundError:
        print(f"File not found: {code_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

