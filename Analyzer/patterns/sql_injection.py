import ast
import re

SIMPLE_SQL_RE = re.compile(
    r"(select\s.*from\s|"
    r"delete\s+from\s|"
    r"insert\s+into\s.*values\s|"
    r"update\s.*set\s)",
    re.IGNORECASE | re.DOTALL,
)


class NodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.parent_stack = []

    def visit(self, node):
        self.parent_stack.append(node)
        super(NodeVisitor, self).visit(node)
        self.parent_stack.pop()

    def get_parent(self):
        if len(self.parent_stack) > 1:
            return self.parent_stack[-2]
        else:
            return None


def _check_string(data):
    return SIMPLE_SQL_RE.search(data) is not None


def _evaluate_ast(node, parent):
    wrapper = None
    statement = ""

    if isinstance(parent, ast.BinOp):
        out = _concat_string(node, parent)
        wrapper = out[0]
        statement = out[1]
    elif (
        isinstance(parent, ast.Attribute)
        and parent.attr == "format"
    ):
        statement = node.s
        wrapper = parent._bandit_parent
    elif hasattr(ast, "JoinedStr") and isinstance(
        parent, ast.JoinedStr
    ):
        substrings = [
            child
            for child in parent.values
            if isinstance(child, ast.Str)
        ]
        if substrings and node == substrings[0]:
            statement = "".join([str(child.s) for child in substrings])
            wrapper = parent._bandit_parent

    if isinstance(wrapper, ast.Call):
        names = ["execute", "executemany"]
        name = _get_called_name(wrapper)
        return (name in names, statement)
    else:
        return (False, statement)


def _concat_string(node, parent):
    parts = []
    while isinstance(parent, ast.BinOp) and parent.op in (ast.Add, ast.Mod):
        parts.append(parent.right if parent.left == node else parent.left)
        node = parent
        parent = node

    if isinstance(parent, ast.Str):
        parts.append(parent)

    parts.reverse()
    return (parent, "".join([str(part.s) for part in parts]))


def _get_called_name(node):
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    elif isinstance(node.func, ast.Name):
        return node.func.id
    else:
        return ""


def find_sql_injection(code):
    tree = ast.parse(code)
    visitor = NodeVisitor()
    visitor.visit(tree)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Str):
            parent = visitor.get_parent()
            val = _evaluate_ast(node, parent)
            if _check_string(val[1]):
                issues.append(
                    {
                        "line": node.lineno,
                        "message": "Possible SQL injection vector through string-based query construction.",
                        "severity": "Medium",
                        "confidence": "Medium" if val[0] else "Low",
                    }
                )

    return issues


def main():
    code_path = input("Enter the path to the Python code file: ")
    try:
        with open(code_path, "r") as file:
            python_code = file.read()
            issues = find_sql_injection(python_code)

            if issues:
                print("\nSQL Injection Issues:")
                for issue in issues:
                    print(
                        f"Line {issue['line']}: {issue['message']} (Severity: {issue['severity']}, Confidence: {issue['confidence']})"
                    )
            else:
                print("No SQL Injection issues found in the provided code.")
    except FileNotFoundError:
        print(f"File not found: {code_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

