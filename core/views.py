from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.core import serializers
from core.models import Course
import json
from bs4 import BeautifulSoup as bs
import mechanicalsoup


def initMajorCourses(year):
    if year >= 2015:
        return [
            [], [],
            ['4190.101', 'M1522.000600', 'M1522.000700'],
            ['4190.206A', '4190.308', 'M1522.000900', '400.000'],
            ['M1522.000100', 'M1522.000800'],
            ['4190.309A', '4190.407'],
            [], [],
        ]
    if year <= 2014 or year >= 2011:
        return [
            [], [],
            ['4190.201', '4190.101', '4190.102A', '4190.202A'],
            ['4190.206A', '4190.204', '4190.210', '400.000'],
            ['4190.307', '4190.308'],
            ['4190.310', '4190.407'],
            [], [],
        ]
    if year <= 2010 or year >= 2008:
        return [
            [], [],
            ['4190.201', '4190.101', '4190.102A', '4190.202A'],
            ['4190.206A', '4190.204', '4190.210', '400.000'],
            ['4190.307', '4190.308'],
            ['4190.310', '4190.407'],
            [], [],
        ]

def replaceable(code):
    replaceables = [
        ['4190.202A', '4190.309A'],
        ['4190.426', '4190.426A'],
        ['4190.201', 'M1522.000700'],
        ['4190.204', 'M1522.000900'],
        ['4190.203', 'M1522.000800'],
        ['4190.102A', 'M1522.000600'],
        ['4190.311A', 'M1522.000200'],
        ['4190.413A', 'M1522.000300'],
        ['400.000', '400.015', '400.013', '400.020', '400.022', '400.023', '400.024'],
    ]
    for sameList in replaceables:
        if code in sameList:
            return sameList
    return [code]

def AdjustCourse(course):
    semester = course['shtmDetaShtm']
    if semester == '여름학기':
        semester = '1학기'
    if semester == '겨울학기':
        semester = '2학기'
    if AdjustCourse.semester_name != course['schyy']+semester:
        AdjustCourse.semester += 1
        AdjustCourse.semester_name = course['schyy']+semester
    name = course['sbjtNm']
    return {
        'code': course['sbjtCd'],
        'name': name,
        'hours': course['acqPnt'],
        'course_type': course['cptnSubmattFgCdNm'],
        'semester': AdjustCourse.semester,
        'mandatory': 'false',
        'done': 'true',
    }

def initGeneralCourses(year):
    return [
        [
            {'name': '외국어', 'subarea': '외국어', 'count': 1},
            {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1']},
            {'name': '과학적 사고와 실험', 'course': ['물리학 1', '물리학 2', '화학 1', '화학 2', '생물학 1', '생물학 2', '물리학', '화학', '생물학'], 'amount': 8},
            {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습']}
        ],
        [
            {'name': '글쓰기의 기초', 'course': ['글쓰기의 기초', '과학과 기술 글쓰기']},
            {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2']},
            {'name': '공학수학 1', 'course': ['공학수학 1']},
            {'name': '과학적 사고와 실험', 'course': ['물리학 1', '물리학 2', '화학 1', '화학 2', '생물학 1', '생물학 2', '물리학', '화학', '생물학'], 'amount': 4},
        ],
        [
            {'name': '공학수학 2', 'course': ['공학수학 2']},
        ],
        [
            {'name': '통계학', 'course': ['통계학']},
            {'name': '통계학실험', 'course': ['통계학실험']},
        ],
        [
            {'name': '외국어', 'subarea': '외국어', 'count': 1},
            {'name': '학문의 세계', 'area': '학문의 세계', 'hours': 3},
        ],
        [
            {'name': '학문의 세계', 'area': '학문의 세계', 'hours': 3},
        ],
        [
            {'name': '사회성 교과목군', 'course': ['기술과 기업', '창업과 경제', '기술과 경제', '공학윤리와 리더십', '특허와 기술창업', '기술과 창업', '현대기술과 윤리적 사고', '공학기술의 역사', '공학인을 위한 경영'], 'subarea': '인간과 사회', 'hours': 3},
        ],
        [
            {'name': '창의성 교과목군', 'course': ['현대도시건축산책', '창조와 디자인', '테크놀러지와 예술: 전시예술공학', '소리의 과학과 악기제작 체험', '창의공학설계', '디지털아트공학', '공학도를 위한 창의적 사고'], 'subarea': '문화와 예술', 'hours': 3},
        ],
    ]

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
    AdjustCourse.semester = -1
    AdjustCourse.semester_name = ''
    result = [AdjustCourse(course) for course in courses['GRD_SCOR401'] if course['mrksGrdCd'] not in ['F', 'U']]
    dept_json = br.post('https://shine.snu.ac.kr/uni/uni/scor/mrtr/findTabCumlMrksYyShtmClsfTtInq01List2.action',
            params={'cscLocale':'ko_KR','strPgmCd':'S030302'}, headers=headers,
            json={"SUN":{"strSchyy":"2016","strShtmFg":"U000200001","strDetaShtmFg":"U000300001","strBdegrSystemFg":"U000100001","strFlag":"all"}}).text
    user_json = br.post('https://shine.snu.ac.kr/com/com/sstm/logn/findUserInfo.action', headers=headers,
            json={"findUsers":{"rType":"3tier","logType":"systemConn","chgUserYn":"N","chgBfUser":"","chgAfUser":""}}).text
    name = json.loads(user_json)['userInfos'][0]['USERNM']
    dept = json.loads(dept_json)['GRD_SCOR402'][0]

    majorCourses = initMajorCourses(int(dept['stuno'][:4]))
    majors = [[] for _ in range(8)]
    for course in result:
        if course['course_type'] in ['전필', '전선']:
            if course['course_type'] == '전필':
                course['mandatory'] = '1'
                for replaceableCourse in replaceable(course['code']):
                    if replaceableCourse in [j for i in majorCourses for j in i]:
                        course['mandatory'] = 'true'
            majors[course['semester']].append(course)
            for replaceableCourse in replaceable(course['code']):
                for semester in range(len(majorCourses)):
                    if replaceableCourse in majorCourses[semester]:
                        majorCourses[semester].remove(replaceableCourse)
    for semester in range(len(majorCourses)):
        for code in majorCourses[semester]:
            course = Course.objects.filter(code=code)[0]
            majors[semester].append({
                'code': code,
                'name': course.name,
                'hours': course.hours,
                'semester': semester,
                'mandatory': 'true',
                'done': 'false',
                })
    must = [
        [{'semester': 3, 'code': '4190.209'}],
        [{'semester': 6, 'code': '4190.422'}],
        [{'semester': 5, 'code': 'M1522.000200'}, {'semester': 6, 'code': 'M1522.000300'}],
    ]

    majorSum = 0
    majorDoneSum = 0
    for semester in majors:
        for course in semester:
            if course['mandatory'] == 'true':
                majorSum += int(course['hours'])
                if course['done'] == 'true':
                    majorDoneSum += int(course['hours'])

    for i in range(len(must)):
        flag = False
        for code in [course['code'] for course in result]:
            for replaceableCourse in replaceable(code):
                if replaceableCourse in [course['code'] for course in must[i]]:
                    flag = True
        if not flag:
            for course in must[i]:
                courseData = Course.objects.filter(code=course['code'])[0]
                majors[course['semester']].append({
                    'code': course['code'],
                    'name': courseData.name,
                    'hours': courseData.hours,
                    'semester': course['semester'],
                    'mandatory': 'true',
                    'done': 'false',
                    })

    # 교양
    generalCourses = initGeneralCourses(int(dept['stuno'][:4]))
    generals = [[] for _ in range(8)]
    for semester in range(len(generalCourses)):
        for rule in generalCourses[semester]:
            if 'area' in rule:
                areaList = [course.code for course in Course.objects.filter(area=rule['area'])]
                for course in result:
                    if course['code'] in areaList:
                        pass
            if 'subarea' in rule:
                pass
            if 'course' in rule:
                pass

    score = sum([course['hours'] for course in result])
    return {'courses': result, 'dept': dept['deptNm'], 'stuno': dept['stuno'], 'majorCourses': majors, 'score': score, 'name': name, 'general': [], 'majorSum': majorSum, 'majorDoneSum': majorDoneSum}

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
        return render(request, 'core/result_horizontal.html', crawlCourse(mysnu_username, mysnu_password))
    return redirect('login')

def coursesJSON(request):
    if request.session.get('mysnu_username', False) and request.session.get('mysnu_password', False):
        mysnu_username = request.session['mysnu_username']
        mysnu_password = request.session['mysnu_password']
        result = crawlCourse(mysnu_username, mysnu_password)
        return JsonResponse(result)
    return JsonResponse(dict())
