from .models import Course
import requests
from bs4 import BeautifulSoup as bs
import xlrd


def CrawlCourse():
    yearList = []
    semesterName = {
        'U000200001U000300001': '1',
        'U000200001U000300002': 'S',
        'U000200002U000300001': '2',
        'U000200002U000300002': 'W'
    }
    searchUrl = 'http://sugang.snu.ac.kr/sugang/cc/cc100.action'
    for year in range(2009, 2017):
        semesterList = []
        for semester in ['U000200001U000300001', 'U000200001U000300002', 'U000200002U000300001', 'U000200002U000300002']:
            areaList = []
            formData = {
                'srchOpenUpSbjtFldCd': '',
                'srchOpenSbjtFldCd': '',
                'srchOpenShtm': semester,
                'srchCond':'1',
                'pageNo':'',
                'workType':'',
                'sortKey':'',
                'sortOrder':'',
                'srchOpenSchyy': str(year),
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
            }
            searchPage = requests.post(searchUrl, data=formData)
            soup = bs(searchPage.text, 'html5lib')
            area = soup.find(id='srchOpenUpSbjtFldCd')
            for area_value in area.find_all('option'):
                formData['srchOpenUpSbjtFldCd'] = area_value['value']
                searchPage = requests.post(searchUrl, data=formData)
                soup = bs(searchPage.text, 'html5lib')
                subarea = soup.find_all('select')[4]
                subareaList = []
                for subarea_value in subarea.find_all('option'):
                    subareaList.append({'name': subarea_value.text.strip(), 'code': subarea_value['value'].strip()})
                areaList.append({'name': area_value.text.strip(), 'code': area_value['value'].strip(), 'subarea': subareaList})
            semesterList.append({'semester': semester, 'area': areaList})
        yearList.append({'year': year, 'semester': semesterList})
    print(yearList)

    excelUrl = 'http://sugang.snu.ac.kr/sugang/cc/cc100excel.action'

    for year in yearList:
        for semester in year['semester']:
            courses = dict()
            for area in semester['area']:
                print(area['name'] + ' : code[' + area['code'] + ']')
                for subarea in area['subarea']:
                    print(subarea['name'] + ' : code[' + subarea['code'] + ']')
                    excel = requests.post(excelUrl, data={
                        'srchOpenUpSbjtFldCd':area['code'],
                        'srchOpenSbjtFldCd':subarea['code'],
                        'srchOpenShtm': semester['semester'],
                        'srchOpenSchyy': str(year['year']),
                        'srchCond':'1',
                        'pageNo':'1',
                        'workType':'EX',
                        'sortKey':'',
                        'sortOrder':'',
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
                        'inputTextView':'',
                        'inputText':''
                        })
                    try:
                        courses_workbook = xlrd.open_workbook(file_contents=excel.content)
                    except Exception as e:
                        print(e)
                        continue
                    courses_sheet = courses_workbook.sheet_by_index(0)
                    print(courses_sheet.nrows)
                    for courses_index in range(3, courses_sheet.nrows):
                        courses[courses_sheet.cell_value(courses_index, 5)] = {
                                'year': year['year'], 'name': courses_sheet.cell_value(courses_index, 7),
                                'hours': courses_sheet.cell_value(courses_index, 9),
                                'area': area['name'] if area['name'] != '전체' else courses_sheet.cell_value(courses_index, 0) if courses_sheet.cell_value(courses_index, 0) in ['전필', '전선'] else '',
                                'subarea': subarea['name'] if subarea['name'] != '전체' else '',
                                'semester': semesterName[semester['semester']]}
            for code, data in courses.items():
                course = Course(
                        code=code, year=data['year'], name=data['name'],
                        hours=data['hours'], area=data['area'], subarea=data['subarea'],
                        semester=data['semester'])
                print(course)
                course.save()
