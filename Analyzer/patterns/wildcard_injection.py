import ast

config = {
    "shell": ["chown", "chmod", "tar", "rsync"]
}

def is_vulnerable_call(node):
    return (
        isinstance(node, ast.Call)
        and (
            (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr in config["shell"]
            )
            or (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
                and node.func.attr in config["shell"]
                and (
                    any(kw.arg == "shell" and kw.value.value is True for kw in node.keywords)
                    or node.check_call_arg_value("shell", "True")
                )
            )
        )
    )

def has_wildcard_argument(node):
    if node.args:
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and "*" in arg.value:
                return True
            elif isinstance(arg, ast.List):
                for elt in arg.elts:
                    if (
                        isinstance(elt, ast.Constant)
                        and isinstance(elt.value, str)
                        and "*" in elt.value
                    ):
                        return True
    return False

def find_wildcard_injection_issues(tree):
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if is_vulnerable_call(node.value) and has_wildcard_argument(node.value):
                issues.append({
                    "line": node.lineno,
                    "severity": "HIGH",
                    "confidence": "MEDIUM",
                    "cwe": "IMPROPER_WILDCARD_NEUTRALIZATION",
                    "text": f"Possible wildcard injection in call: {ast.dump(node)}",
                })

    return issues
