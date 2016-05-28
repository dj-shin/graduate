from .models import Area, Course, CourseAcquired, Department, Rule
import requests
from bs4 import BeautifulSoup as bs
import xlrd


def cseCrawl():
    url = 'http://cse.snu.ac.kr/undergraduate/courses'
    r = requests.get(url)
    soup = bs(r.text, 'html5lib')
    table = soup.table
    for course in table.tbody.find_all('tr'):
        extract = []
        for td in course.find_all('td'):
            content = td.string
            if content != None:
                content = content.strip()
            if td.a != None:
                content = td.a.string.strip()
            extract.append(content)
        
        course = Course()
        course.area = None
        if extract[0] == '교양':
            course.course_type = None
        elif extract[0] == '전공필수':
            course.course_type = Course.MANDATORY
        elif extract[0] == '전공선택':
            course.course_type = Course.ELECTIVE
        course.code = extract[1]
        course.name = extract[2]
        course.hours = int(extract[3])

        course.save()

def CrawlExcel():
    excelUrl = 'http://sugang.snu.ac.kr/sugang/cc/cc100excel.action'
    areaList = [
        { 
            'code': '04',
            'name': '학문의 기초',
            'subarea': [
                {'code': '40', 'name': '사고와 표현'},
                {'code': '41', 'name': '외국어'},
                {'code': '42', 'name': '수량적 분석과 추론'},
                {'code': '43', 'name': '과학적 사고와 실험'},
                {'code': '44', 'name': '컴퓨터와 정보 활용'},
            ]
        },
        {
            'code': '05',
            'name': '학문의 세계',
            'subarea': [
                {'code': '45', 'name': '언어와 문학'},
                {'code': '46', 'name': '문화와 예술'},
                {'code': '47', 'name': '역사와 철학'},
                {'code': '48', 'name': '정치와 경제'},
                {'code': '49', 'name': '인간과 사회'},
                {'code': '50', 'name': '자연과 기술'},
                {'code': '51', 'name': '생명과 환경'},
            ]
        },
        {
            'code': '06',
            'name': '선택교양',
            'subarea': [
                {'code': '52', 'name': '체육'},
                {'code': '53', 'name': '예술 실기'},
                {'code': '54', 'name': '대학과 리더십'},
                {'code': '55', 'name': '창의와 융합'},
                {'code': '56', 'name': '한국의 이해'},
            ]
        },
        {
            'code': '',
            'name': '',
            'subarea': [
                {'code': '', 'name': ''},
            ]
        },
    ]
    result = dict()

    for area in areaList:
        print(area['name'])
        for subarea in area['subarea']:
            print(subarea['name'])
            for semester in ['U000200001U000300001', 'U000200001U000300002', 'U000200002U000300001', 'U000200002U000300002']:
                excel = requests.post(excelUrl, data={
                    'srchOpenUpSbjtFldCd':area['code'],
                    'srchOpenSbjtFldCd':subarea['code'],
                    'srchOpenShtm': semester,
                    'srchCond':'1',
                    'pageNo':'1',
                    'workType':'EX',
                    'sortKey':'',
                    'sortOrder':'',
                    'srchOpenSchyy':'2015',
                    'currSchyy':'2016',
                    'currShtmNm':'여름학기',
                    'srchCptnCorsFg':'',
                    'srchOpenShyr':'',
                    'srchSbjtCd':'',
                    'srchSbjtNm':'',
                    'srchOpenUpDeptCd':'',
                    'srchOpenDeptCd':'',
                    'srchOpenMjCd':'',
                    'srchOpenSubmattCorsFg':'',
                    'srchOpenSubmattFgCd':'',
                    'srchOpenPntMin':'',
                    'srchOpenPntMax':'',
                    'srchCamp':'',
                    'srchBdNo':'',
                    'srchProfNm':'',
                    'srchTlsnAplyCapaCntMin':'',
                    'srchTlsnAplyCapaCntMax':'',
                    'srchTlsnRcntMin':'',
                    'srchTlsnRcntMax':'',
                    'srchOpenSbjtTmNm':'',
                    'srchOpenSbjtTm':'',
                    'srchOpenSbjtTmVal':'',
                    'srchLsnProgType':'',
                    'srchMrksGvMthd':'',
                    'srchFlag':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'openSchyy':'',
                    'openShtmFg':'',
                    'openDetaShtmFg':'',
                    'sbjtCd':'',
                    'ltNo':'',
                    'inputTextView':'',
                    'inputText':''
                    })
                try:
                    courses_workbook = xlrd.open_workbook(file_contents=excel.content)
                except Exception:
                    continue
                courses_sheet = courses_workbook.sheet_by_index(0)
                for courses_index in range(3, courses_sheet.nrows):
                    if not courses_sheet.cell_value(courses_index, 5) in result:
                        result[courses_sheet.cell_value(courses_index, 5)] = {
                            'name': courses_sheet.cell_value(courses_index, 7),
                            'hours': courses_sheet.cell_value(courses_index, 9),
                            'area': area['name'] + ' - ' + subarea['name'] if area['name'] else None,
                            'course_type': courses_sheet.cell_value(courses_index, 0) if courses_sheet.cell_value(courses_index, 0) in ['전필', '전선'] else None,
                        }

    for code in result.keys():
        course = Course()
        (area, created) = Area.objects.get_or_create(name=result[code]['area']) if result[code]['area'] else (None, False)
        course.area = area
        course.code = code
        course.name = result[code]['name']
        course.hours = result[code]['hours']
        if result[code]['course_type'] == '전필':
            course.course_type = Course.MANDATORY
        elif result[code]['course_type'] == '전선':
            course.course_type = Course.ELECTIVE
        else:
            course.course_type = None

        try:
            presentCourse = Course.objects.get(pk=code)
        except Exception:
            pass
        else:
            presentCourse.delete()

        course.save()
