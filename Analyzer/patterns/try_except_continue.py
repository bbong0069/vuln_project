import ast

def try_except_continue_code(tree):
    issues = []

    for node in ast.walk(tree): 
        if isinstance(node, ast.ExceptHandler): #예외 처리 블록인 경우
            for inner_node in node.body:
                if isinstance(inner_node, ast.Continue): #Continue 문 포함하는 경우
                    issues.append({
                        "line": inner_node.lineno,
                        "severity": "LOW", #심각도 낮음
                        "confidence": "HIGH", #신뢰도 높음
                        "cwe": "IMPROPER_CHECK_OF_EXCEPT_COND", #CWE 코드
                        "text": "Try, Except, Continue detected.", #취약점 메세지
                    })

    return issues
