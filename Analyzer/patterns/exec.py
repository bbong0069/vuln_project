import ast

def _check_exec(node): #함수 이름이 'exec'인거 확인 
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Name) and node.value.func.id == "exec"

<<<<<<< HEAD
def find_exec_usage(tree):
=======
def find_exec_usage(code):
    tree = ast.parse(code) #입력 코드 ast파싱 (애초에 ast된 거를 넣어도 될 듯)
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
    issues = []

    for node in ast.walk(tree):
        if _check_exec(node): #'exec' 함수 찾기
            issues.append(
                {
                    "line": node.lineno, #줄 번호
                    "message": "Use of exec detected.", #이슈 나타내는 메세지
                    "severity": "Medium", #이슈 심각 수준
                    "confidence": "High", #이슈 감지하는 신뢰 수준
                }
            )

    return issues 
