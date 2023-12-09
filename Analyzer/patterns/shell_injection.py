import ast

def has_shell(node):
<<<<<<< HEAD
    # 함수 호출에 "shell" 키워드가 있는지 확인
    keywords = node.keywords
    result = False
    if any(keyword.arg == "shell" for keyword in keywords):
        # "shell" 키워드가 있다면 해당 값에 따라 결과를 설정
        for key in keywords:
            if key.arg == "shell":
                val = key.value
                # 값의 타입에 따라 결과를 설정
=======
    keywords = node.keywords
    result = False
    if any(keyword.arg == "shell" for keyword in keywords):
        for key in keywords:
            if key.arg == "shell":
                val = key.value
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
    # 첫 번째 인수가 문자열이면 "LOW", 아니면 "HIGH" 반환
		# LOW인 이유 : 문자열 포맷팅, 변수 삽입 없이 직접 주어진 경우로 간주되어 상대적으로 안전
		# HIGH인 이유 : 다른 변수나 외부 입력을 통해 동적으로 생성되었을 가능성이 있어 취약성이 높다고 판단 
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
    no_formatting = isinstance(node.args[0], ast.Str)
    if no_formatting:
        return "LOW"
    else:
        return "HIGH"

<<<<<<< HEAD
def find_shell_issues(tree):
=======
def find_shell_issues(tree, config):
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
            # subprocess 모듈을 사용한 함수 호출이 있을 경우
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
            if has_shell(node):
                if len(node.args) > 0:
                    sev = _evaluate_shell_call(node)
                    if sev == "LOW":
<<<<<<< HEAD
                        # shell=True가 있지만 안전해 보일 때
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
                        # shell=True이고 보안 문제가 있을 때
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
        elif (# os 모듈을 사용한 os.system 함수 호출이 있을 경우
=======
        elif (
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
            isinstance(node, ast.Call)
            and hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "os"
            and hasattr(node.func, "attr")
            and node.func.attr == "system"
        ):
<<<<<<< HEAD
            
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
        elif (  # system 함수 호출
=======
        elif (
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == "system"
            and isinstance(node.func.ctx, ast.Load)
        ):
<<<<<<< HEAD
          
=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
        elif ( #commands
=======
        elif (
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
            isinstance(node, ast.Call)
            and hasattr(node.func, "value")
            and hasattr(node.func.value, "id")
            and node.func.value.id == "commands"
            and hasattr(node.func, "attr")
            and node.func.attr in ["getoutput", "getstatusoutput"]
        ):
<<<<<<< HEAD

=======
>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
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
<<<<<<< HEAD
=======

>>>>>>> 02c318af00be91425f2890fa9f5c3a6aa3f8abd4
