import ast

def _check_yaml_load(node):
    if isinstance(node, ast.Call): #노드가 함수 호출 구조인지 확인
        if (
            hasattr(node.func, "value") 
            and hasattr(node.func.value, "id")
            and node.func.value.id == "yaml"
            and hasattr(node.func, "attr")
            and node.func.attr == "load" #yalm.load인지 확인
            and not any(
                arg.arg == "Loader" and arg.value.id == "SafeLoader"
                for arg in node.keywords
            )
        ):
            return True
    return False

def find_yaml_load_usage(tree): #AST 순회하며 찾기
    issues = []

    for node in ast.walk(tree):
        if _check_yaml_load(node):
            issues.append(
                {
                    "line": node.lineno, #라인 넘버
                    "message": "Use of unsafe yaml load. Allows instantiation of"
                               " arbitrary objects. Consider yaml.safe_load().",
                    "severity": "Medium", #문제 심각도
                    "confidence": "High", #문제를 감지하는 신뢰 수준
                }
            )

    return issues

