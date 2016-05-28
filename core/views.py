from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.core import serializers
from core.models import Area, Course, CourseAcquired, Rule, Department
from core.checker import ApplyRule
from core.crawler import cseCrawl
import json
from bs4 import BeautifulSoup as bs
import mechanicalsoup


def test_basic_success(request):
    success = [
        CourseAcquired('이산수학'),
        CourseAcquired('전기전자회로'),
        CourseAcquired('프로그래밍의 원리'),
        CourseAcquired('운영체제'),
        CourseAcquired('컴퓨터구조'),
        CourseAcquired('프로그래밍언어'),
        CourseAcquired('알고리즘'),
        CourseAcquired('컴퓨터프로그래밍'),
        CourseAcquired('논리설계'),
        CourseAcquired('자료구조')
    ]
    result = [rule.toJSON() for rule in ApplyRule(Rule.objects.all(), success)]
    return HttpResponse(result)

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
    dept = json.loads(dept_json)['GRD_SCOR402'][0]
    return {'courses': result, 'dept': dept}

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
        return render(request, 'core/courses.html')
    return redirect('login')

def coursesJSON(request):
    if request.session.get('mysnu_username', False) and request.session.get('mysnu_password', False):
        mysnu_username = request.session['mysnu_username']
        mysnu_password = request.session['mysnu_password']
        result = crawlCourse(mysnu_username, mysnu_password)
        return JsonResponse(result)
    return JsonResponse(dict())
