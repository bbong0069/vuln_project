import ast
import re

# 하드코딩된 비밀번호를 검색하기 위한 정규표현식 패턴
RE_WORDS = "(pas+wo?r?d|pass(phrase)?|pwd|token|secrete?)"
RE_CANDIDATES = re.compile(
    "(^{0}$|_{0}_|^{0}_|_{0}$)".format(RE_WORDS), re.IGNORECASE
)

def is_password_candidate(name):
		#변수 이름이 비밀번호로 간주되는지 확인
    return RE_CANDIDATES.search(name) is not None

# return할 issue 정보
def report_issue(node, value):
    return {
        "severity": "Low",
        "confidence": "Medium",
        "cwe": "CWE-259",
        "text": f"Possible hardcoded password: '{value}'",
        "location": f"Line {node.lineno}",
    }

#부모 노드 찾는 함수
def find_assign_parent(tree, node):
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            if child == node:
                return parent if parent else None
    return None

#문자열 리터럴 체크 함수
def check_string_literal(node, tree):
    parent = find_assign_parent(tree, node)
    #변수에 할당된 경우
    if parent and isinstance(parent, ast.Assign):
        for target in parent.targets: 
            if isinstance(target, ast.Name) and is_password_candidate(target.id): #변수 이름이 비밀번호로 간주되면
                return report_issue(node, node.s)
            elif isinstance(target, ast.Attribute) and is_password_candidate(target.attr):#속성에 할당된 경우도 확인
                return report_issue(node, node.s)
    #리스트 또는 딕셔너리에 할당된 경우
    elif parent and isinstance(parent, ast.Subscript) and is_password_candidate(node.s):
        assign = parent.value
        if isinstance(assign, ast.Str): #문자열이라면 
            return report_issue(node, assign.s)
    #리스트의 인덱스로 사용된 경우
    elif parent and isinstance(parent, ast.Index) and is_password_candidate(node.s):
        assign = parent.value.value
        if isinstance(assign, ast.Str):#문자열이라면
            return report_issue(node, assign.s)
    #비교 연산에서 사용된 경우
    elif parent and isinstance(parent, ast.Compare):
        comp = parent
        if isinstance(comp.left, ast.Name) and is_password_candidate(comp.left.id):#변수 이름이 비밀번호로 간주되면
            if isinstance(comp.comparators[0], ast.Str):
                return report_issue(node, comp.comparators[0].s)
        elif isinstance(comp.left, ast.Attribute) and is_password_candidate(comp.left.attr):#속성에 할당된 경우도 확인
            if isinstance(comp.comparators[0], ast.Str):
                return report_issue(node, comp.comparators[0].s)

#함수 호출에서 문자열 인자가 있는지 확인
def check_function_argument(node, parent):
    if isinstance(parent, ast.Call):
        for kw in parent.keywords:
            if isinstance(kw.value, ast.Str) and is_password_candidate(kw.arg):#함수 호출에서 문자열 인자가 비밀번호라면
                return report_issue(node, kw.value.s)

#함수 정의에서 기본값 있는지 확인
def check_default_argument(node):
    defs = [None] * (len(node.args.args) - len(node.args.defaults))
    defs.extend(node.args.defaults)

    for key, val in zip(node.args.args, defs):
        #함수 정의에서 기본값이 비밀번호라면
        if isinstance(key, (ast.Name, ast.arg)) and isinstance(val, ast.Str) and is_password_candidate(key.arg):
            return report_issue(node, val.s)

#주어진 코드 분석해 issue 리턴
def hardcoded_password_usage(tree):
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Str): 
            issue = check_string_literal(node, tree) #문자열 리터럴에서 확인
            if issue:
                issues.append(issue)
        elif isinstance(node, ast.Call): #함수 호출 확인
            issue = check_function_argument(node, find_assign_parent(tree, node))
            if issue:
                issues.append(issue)
        elif isinstance(node, ast.FunctionDef): #함수 정의 확인
            issue = check_default_argument(node)
            if issue:
                issues.append(issue)

    return issues
