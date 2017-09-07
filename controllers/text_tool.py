import re

def format_comment_by_expr(text, expresion, replace):
    task_regex_group = re.search(expresion, text)
    print("text")
    print(task_regex_group.group(1))
    print(re.sub(expresion, '', text))
    return {'message':re.sub(expresion, '', text), 'artifact_id':task_regex_group.group(1)}