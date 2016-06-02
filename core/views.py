from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.core import serializers
from core.models import Area, Course, CourseAcquired, Rule, Department
from core.checker import ApplyRule
from core.crawler import cseCrawl
import json
from bs4 import BeautifulSoup as bs
import mechanicalsoup


def index(request):
    return redirect('courses')

def AdjustCourse(course):
    return {
        'code': course['sbjtCd'],
        'name': course['sbjtNm'],
        'hours': course['acqPnt'],
        'course_type': course['cptnSubmattFgCdNm']
    }

def crawlCourse(username, password):
    br = mechanicalsoup.Browser()
    login_page = br.get('http://my.snu.ac.kr/mysnu/portal/MS010/MAIN')
    login_form = login_page.soup.select('#LoginForm')[0]
    login_form.select('#si_id')[0]['value'] = username
    login_form.select('#si_pwd')[0]['value'] = password
    redirect_page = br.submit(login_form, login_page.url)
    redirect_form = redirect_page.soup.select('form')[0]
    br.submit(redirect_form, 'http://sso.snu.ac.kr/nls3/fcs')
    br.get('http://my.snu.ac.kr/mysnu/portal/MS010/MAIN')
    br.get('http://my.snu.ac.kr/mysnu/login?loginType=auto')
    br.get('https://shine.snu.ac.kr/com/ssoLoginForSWAction.action',
        params={'systemCd':'S', 'pgmCd':'S030302', 'unitBussCd':'03','lanCd':'ko', 'lang_knd':'ko','evSecurityCode':'EV_SECURITY_CODE_1463911122502'})
    headers = {
        'Host': 'shine.snu.ac.kr',
        'Connection': 'keep-alive',
        'Content-Length': '129',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://shine.snu.ac.kr',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/extJs+sua; charset=UTF-8',
        'Referer': 'https://shine.snu.ac.kr/com/mybsvr/webContainer.html?snu_=a298UzAzMDMwMnzrgpjsnZjshLHsoIF8L3NoaW5lL3VuaS9zY29yL21ydHJ8Q3VtbE1ya3NZeVNodG1DbHNmVHRJbnEuaHRtbHw5fDQ=',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    }
    grade_json = br.post('https://shine.snu.ac.kr/uni/uni/scor/mrtr/findTabCumlMrksYyShtmClsfTtInq02.action',
            params={'cscLocale':'ko_KR','strPgmCd':'S030302'}, headers=headers,
            json={"SUN":{"strSchyy":"2016","strShtmFg":"U000200001","strDetaShtmFg":"U000300001","strBdegrSystemFg":"U000100001","strFlag":"all"}}).text
    courses = json.loads(grade_json)
    result = [AdjustCourse(course) for course in courses['GRD_SCOR401']]
    dept_json = br.post('https://shine.snu.ac.kr/uni/uni/scor/mrtr/findTabCumlMrksYyShtmClsfTtInq01List2.action',
            params={'cscLocale':'ko_KR','strPgmCd':'S030302'}, headers=headers,
            json={"SUN":{"strSchyy":"2016","strShtmFg":"U000200001","strDetaShtmFg":"U000300001","strBdegrSystemFg":"U000100001","strFlag":"all"}}).text
    user_json = br.post('https://shine.snu.ac.kr/com/com/sstm/logn/findUserInfo.action', headers=headers,
            json={"findUsers":{"rType":"3tier","logType":"systemConn","chgUserYn":"N","chgBfUser":"","chgAfUser":""}}).text
    name = json.loads(user_json)['userInfos'][0]['USERNM']
    dept = json.loads(dept_json)['GRD_SCOR402'][0]
    majorCourses = [
        {'name': '컴퓨터프로그래밍', 'x': 10, 'y': 90, 'mandatory': 'true'},
        {'name': '프로그래밍의 원리', 'x': 170, 'y': 90, 'mandatory': 'false'},
        {'name': '프로그래밍언어', 'x': 480, 'y': 90, 'mandatory': 'false'},
        {'name': '소프트웨어 개발의 원리와 실제 ', 'x': 325, 'y': 140, 'mandatory': 'true'},
        {'name': '소프트웨어공학', 'x': 640, 'y': 150, 'mandatory': 'false'},
        {'name': '오토마타이론', 'x': 325, 'y': 205, 'mandatory': 'false'},
        {'name': '컴파일러', 'x': 640, 'y': 205, 'mandatory': 'false'},
        {'name': '데이터마이닝 개론', 'x': 325, 'y': 260, 'mandatory': 'false'},
        {'name': '알고리즘', 'x': 480, 'y': 300, 'mandatory': 'true'},
        {'name': '이산수학', 'x': 10, 'y': 350, 'mandatory': 'true'},
        {'name': '자료구조', 'x': 170, 'y': 350, 'mandatory': 'true'},
        {'name': '데이터베이스', 'x': 480, 'y': 350, 'mandatory': 'false'},
        {'name': '인공지능', 'x': 640, 'y': 385, 'mandatory': 'false'},
        {'name': '데이터통신', 'x': 480, 'y': 435, 'mandatory': 'false'},
        {'name': '컴퓨터네트워크', 'x': 640, 'y': 435, 'mandatory': 'false'},
        {'name': '컴퓨터그래픽스', 'x': 640, 'y': 487, 'mandatory': 'false'},
        {'name': '공학수학 1', 'x': 10, 'y': 560, 'mandatory': 'true'},
        {'name': '선형 및 비선형 계산모델', 'x': 325, 'y': 500, 'mandatory': 'false'},
        {'name': '디지털신호처리', 'x': 325, 'y': 560, 'mandatory': 'false'},
        {'name': '논리설계', 'x': 10, 'y': 620, 'mandatory': 'true'},
        {'name': '전기전자회로', 'x': 170, 'y': 595, 'mandatory': 'true'},
        {'name': '컴퓨터구조', 'x': 170, 'y': 645, 'mandatory': 'true'},
        {'name': '시스템프로그래밍', 'x': 325, 'y': 645, 'mandatory': 'true'},
        {'name': '하드웨어시스템설계', 'x': 480, 'y': 595, 'mandatory': 'true'},
        {'name': '운영체제', 'x': 480, 'y': 645, 'mandatory': 'false'},
    ]
    score = sum([course['hours'] for course in result])
    namelist = [course['name'] for course in result]
    for majorCourse in majorCourses:
        if majorCourse['name'] in namelist:
            majorCourse['done'] = 'true'
        else:
            majorCourse['done'] = 'false'
    general = [course for course in result if course['course_type'] == '교양']
    for course in general:
        try:
            course['area'] = Course.objects.get(pk=course['code']).area.name
        except Exception:
            course['area'] = ''
    general = dict()
    for area in Area.objects.all():
        courses = []
        for course in result:
            try:
                if area == Course.objects.get(pk=course['code']).area:
                    courses.append(course)
            except Exception:
                pass
        if courses:
            general[area.name] = {
                'courses': ', '.join([course['name'] for course in courses]),
                'hours': sum([int(course['hours']) for course in courses]),
            }
    return {'courses': result, 'dept': dept['deptNm'], 'stuno': dept['stuno'], 'majorCourses': majorCourses, 'score': score, 'name': name, 'general': general}

def login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')
    elif request.method == 'POST':
        data = QueryDict(request.body)
        mysnu_username = data['username']
        mysnu_password = data['password']
        request.session['mysnu_username'] = mysnu_username
        request.session['mysnu_password'] = mysnu_password
        return redirect('courses')

def courses(request):
    if request.session.get('mysnu_username', False) and request.session.get('mysnu_password', False):
        # return render(request, 'core/courses.html')
        mysnu_username = request.session['mysnu_username']
        mysnu_password = request.session['mysnu_password']
        return render(request, 'core/result.html', crawlCourse(mysnu_username, mysnu_password))
    return redirect('login')

def coursesJSON(request):
    if request.session.get('mysnu_username', False) and request.session.get('mysnu_password', False):
        mysnu_username = request.session['mysnu_username']
        mysnu_password = request.session['mysnu_password']
        result = crawlCourse(mysnu_username, mysnu_password)
        return JsonResponse(result)
    return JsonResponse(dict())
