import ast

def _check_eval(node): #함수 이름이 'eval'인거 확인 
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Name) and node.value.func.id == "eval"

def find_eval_usage(tree):
    issues = []

    for node in ast.walk(tree):
        if _check_eval(node): #'eval' 함수 찾기
            issues.append(
                {
                    "line": node.lineno, #줄 번호
                    "message": "Use of exec detected.", #이슈 나타내는 메세지
                    "severity": "Medium", #이슈 심각 수준
                    "confidence": "High", #이슈 감지하는 신뢰 수준
                }
            )

    return issues 
