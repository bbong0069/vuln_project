import ast

#pickle.loads 탐지
def _check_pickle_loads(node):
    if isinstance(node, ast.Call): #노드가 함수 호출 구조인지 확인
        if (
            hasattr(node.func, "value") 
            and hasattr(node.func.value, "id")
            and node.func.value.id == "pickle"
            and hasattr(node.func, "attr")
            and node.func.attr == "loads" #pickle.load인지 확인
            ):
            return True
        return False

#pickle.dump 탐지
def _check_pickle_dump(node):
    if isinstance(node, ast.Call): #노드가 함수 호출 구조인지 확인
        if (
            hasattr(node.func, "value") 
            and hasattr(node.func.value, "id")
            and node.func.value.id == "pickle"
            and hasattr(node.func, "attr")
            and node.func.attr == "dump" #pickle.dumps인지 확인
            ):
            return True
        return False
      
def pickle_usage(tree):
    issues = []

    for node in ast.walk(tree):
        if _check_pickle_loads(node):
            issues.append({
                "line": node.lineno,
                "message": "Use of pickle.loads() detected.",
                "severity": "High",
                "confidence": "High",
            })
        elif _check_pickle_dump(node):
            issues.append({
                "line": node.lineno,
                "message": "Use of pickle.dump() detected.",
                "severity": "High",
                "confidence": "High",
            })
            

    return issues
