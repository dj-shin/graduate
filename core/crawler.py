from .models import Area, Course, CourseAcquired, Department, Rule
import requests
from bs4 import BeautifulSoup as bs


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

