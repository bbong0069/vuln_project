import ast

def has_shell(node):
    keywords = node.keywords
    result = False
    if any(keyword.arg == "shell" for keyword in keywords):
        for key in keywords:
            if key.arg == "shell":
                val = key.value
                if isinstance(val, ast.Num):
                    result = bool(val.n)
                elif isinstance(val, ast.List):
                    result = bool(val.elts)
                elif isinstance(val, ast.Dict):
                    result = bool(val.keys)
                elif isinstance(val, ast.Name) and val.id in ["False", "None"]:
                    result = False
                elif isinstance(val, ast.NameConstant):
                    result = val.value
                else:
                    result = True
    return result

def _evaluate_shell_call(node):
    no_formatting = isinstance(node.args[0], ast.Str)
    if no_formatting:
        return "LOW"
    else:
        return "HIGH"

def find_shell_issues(tree, config):
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "subprocess"
            and hasattr(node.func, "attr")
            and node.func.attr in ["Popen", "call", "check_call", "check_output", "run"]
        ):
            if has_shell(node):
                if len(node.args) > 0:
                    sev = _evaluate_shell_call(node)
                    if sev == "LOW":
                        issues.append(
                            {
                                "line": node.lineno,
                                "message": "subprocess call with shell=True seems safe, but "
                                "may be changed in the future, consider "
                                "rewriting without shell",
                                "severity": "LOW",
                                "confidence": "HIGH",
                                "cwe": "OS_COMMAND_INJECTION",
                            }
                        )
                    else:
                        issues.append(
                            {
                                "line": node.lineno,
                                "message": "subprocess call with shell=True identified, "
                                "security issue.",
                                "severity": "HIGH",
                                "confidence": "HIGH",
                                "cwe": "OS_COMMAND_INJECTION",
                            }
                        )
        elif (
            isinstance(node, ast.Call)
            and hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "os"
            and hasattr(node.func, "attr")
            and node.func.attr == "system"
        ):
            if has_shell(node):
                issues.append(
                    {
                        "line": node.lineno,
                        "message": f"os.system call with shell=True identified, "
                        "security issue.",
                        "severity": "HIGH",
                        "confidence": "HIGH",
                        "cwe": "OS_COMMAND_INJECTION",
                    }
                )
        elif (
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == "system"
            and isinstance(node.func.ctx, ast.Load)
        ):
            if has_shell(node):
                issues.append(
                    {
                        "line": node.lineno,
                        "message": f"os.system call with shell=True identified, "
                        "security issue.",
                        "severity": "HIGH",
                        "confidence": "HIGH",
                        "cwe": "OS_COMMAND_INJECTION",
                    }
                )
        elif (
            isinstance(node, ast.Call)
            and hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "commands"
            and hasattr(node.func, "attr")
            and node.func.attr in ["getoutput", "getstatusoutput"]
        ):
            if has_shell(node):
                issues.append(
                    {
                        "line": node.lineno,
                        "message": f"{node.func.attr} call with shell=True identified, "
                        "security issue.",
                        "severity": "HIGH",
                        "confidence": "HIGH",
                        "cwe": "OS_COMMAND_INJECTION",
                    }
                )

    return issues

