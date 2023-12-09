import ast

def _check_yaml_load(node):
    if isinstance(node, ast.Call):
        if (
            hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "yaml"
            and hasattr(node.func, "attr")
            and node.func.attr == "load"
            and not any(
                arg.arg == "Loader" and arg.value.id == "SafeLoader"
                for arg in node.keywords
            )
        ):
            return True
    return False

def find_yaml_load_usage(code):
    tree = ast.parse(code)
    issues = []

    for node in ast.walk(tree):
        if _check_yaml_load(node):
            issues.append(
                {
                    "line": node.lineno,
                    "message": "Use of unsafe yaml load. Allows instantiation of"
                               " arbitrary objects. Consider yaml.safe_load().",
                    "severity": "Medium",
                    "confidence": "High",
                }
            )

    return issues

