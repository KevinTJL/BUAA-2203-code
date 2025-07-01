import time
import requests
from bs4 import BeautifulSoup
from getpass import getpass
from urllib.parse import quote
from form import fill_form
import sys

session = requests.Session()

PJXT_URL = "https://spoc.buaa.edu.cn/pjxt/"
LOGIN_URL = f'https://sso.buaa.edu.cn/login?service={quote(PJXT_URL, "utf-8")}cas'

def get_token():
    try:
        response = session.get(LOGIN_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': 'execution'})['value']
        return token
    except Exception:
        print('获取登录令牌失败')
        sys.exit(1)

def login(username, password):
    try:
        form = {
            'username': username,
            'password': password,
            'execution': get_token(),
            '_eventId': 'submit',
            'type': 'username_password',
            'submit': "LOGIN"
        }
        response = session.post(LOGIN_URL, data=form, allow_redirects=True)
        response.raise_for_status()
        if '综合评教系统' in response.text:
            return True
        else:
            return False
    except Exception:
        return False

def get_latest_task():
    try:
        task_list_url = f'{PJXT_URL}personnelEvaluation/listObtainPersonnelEvaluationTasks?pageNum=1&pageSize=1'
        response = session.get(task_list_url)
        response.raise_for_status()
        task_json = response.json()
        if task_json['result']['total'] == 0:
            return None
        return (task_json['result']['list'][0]['rwid'], task_json['result']['list'][0]['rwmc'])
    except Exception:
        print('获取最新任务失败')
        sys.exit(1)

def get_questionnaire_list(task_id):
    try:
        list_url = f'{PJXT_URL}evaluationMethodSix/getQuestionnaireListToTask?rwid={task_id}&pageNum=1&pageSize=999'
        response = session.get(list_url)
        response.raise_for_status()
        return response.json()['result']
    except Exception:
        print('获取问卷列表失败')
        return []

def set_evaluating_method(qinfo):
    try:
        if qinfo['msid'] in ['1', '2']:
            url = f'{PJXT_URL}evaluationMethodSix/reviseQuestionnairePattern'
        elif qinfo['msid'] is None:
            url = f'{PJXT_URL}evaluationMethodSix/confirmQuestionnairePattern'
        else:
            print(f"未知的msid {qinfo['msid']} 对于 {qinfo['wjmc']}")
            return
        form = {
            'wjid': qinfo['wjid'],
            'msid': 1,
            'rwid': qinfo['rwid']
        }
        response = session.post(url, json=form)
        response.raise_for_status()
    except Exception:
        print(f"设置评教方式失败: {qinfo['wjmc']}")

def get_course_list(qid):
    try:
        course_list_url = f'{PJXT_URL}evaluationMethodSix/getRequiredReviewsData?sfyp=0&wjid={qid}&pageNum=1&pageSize=999'
        response = session.get(course_list_url)
        response.raise_for_status()
        course_list_json = response.json()
        return course_list_json.get('result', [])
    except Exception:
        print(f"获取课程列表失败: {qid}")
        return []

def evaluate_single_course(cinfo, method):
    try:
        params = {
            'rwid': cinfo["rwid"],
            'wjid': cinfo["wjid"],
            'sxz': cinfo["sxz"],
            'pjrdm': cinfo["pjrdm"],
            'pjrmc': cinfo["pjrmc"],
            'bpdm': cinfo["bpdm"],
            'bpmc': cinfo["bpmc"],
            'kcdm': cinfo["kcdm"],
            'kcmc': cinfo["kcmc"],
            'rwh': cinfo["rwh"]
        }
        topic_url = f'{PJXT_URL}evaluationMethodSix/getQuestionnaireTopic?' + '&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])
        response = session.get(topic_url)
        response.raise_for_status()
        topic_json = response.json()
        if not topic_json['result']:
            print(f"获取评教主题失败: {cinfo['kcmc']}")
            return
        evaluate_result = fill_form(topic_json['result'][0], method)
        submit_url = f'{PJXT_URL}evaluationMethodSix/submitSaveEvaluation'
        submit_response = session.post(submit_url, json=evaluate_result)
        submit_response.raise_for_status()
        if submit_response.json().get('msg') == '成功':
            print(f"成功评教课程: {cinfo['kcmc']}")
        else:
            print(f"评教失败: {cinfo['kcmc']}")
            sys.exit(1)
    except Exception:
        print(f"评教过程中出错: {cinfo['kcmc']}")
        sys.exit(1)

def auto_evaluate(method):
    task = get_latest_task()
    if task is None:
        print('当前没有可评教的任务')
        return
    print(f"开始评教任务: {task[1]}")
    q_list = get_questionnaire_list(task[0])
    for q in q_list:
        print(f"开始评教问卷: {q['wjmc']}")
        set_evaluating_method(q)
        c_list = get_course_list(q['wjid'])
        for c in c_list:
            if c['ypjcs'] == c['xypjcs']:
                continue
            print(f"评教课程: {c['kcmc']}")
            evaluate_single_course(c, method)
            time.sleep(1)
    print('评教任务完成')

def main():
    username = input('请输入用户名: ')
    password = getpass('请输入密码: ')
    print('正在登录...')
    if login(username, password):
        print('登录成功！')
        print('请选择评教方法:')
        print('1. 最佳评价')
        print('2. 随机评价')
        print('3. 最差及格评价')
        choice = input('请输入选择的数字（默认1）: ').strip()
        if choice == '2':
            method = 'random'
        elif choice == '3':
            method = 'worst_passing'
        else:
            method = 'good'
        auto_evaluate(method)
    else:
        print('登录失败！')
        sys.exit(1)

if __name__ == '__main__':
    main()
