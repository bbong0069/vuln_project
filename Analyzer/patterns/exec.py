import ast

def _check_exec(node):
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Name) and node.value.func.id == "exec"

def find_exec_usage(code):
    tree = ast.parse(code)
    issues = []

    for node in ast.walk(tree):
        if _check_exec(node):
            issues.append(
                {
                    "line": node.lineno,
                    "message": "Use of exec detected.",
                    "severity": "Medium",
                    "confidence": "High",
                }
            )

    return issues

