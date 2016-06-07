from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.core import serializers
from core.models import Course
import json
from bs4 import BeautifulSoup as bs
import mechanicalsoup
import requests


def initMajorCourses(year):
    if year >= 2015:
        return [
            [], [],
            [
                {'name': '컴퓨터프로그래밍', 'course': ['컴퓨터프로그래밍'], 'hours': 4},
                {'name': '이산수학', 'course': ['이산수학'], 'hours': 3},
                {'name': '논리설계', 'course': ['논리설계'], 'hours': 4},
            ],
            [
                {'name': '전기전자회로', 'course': ['전기전자회로'], 'hours': 3},
                {'name': '컴퓨터구조', 'course': ['컴퓨터구조'], 'hours': 3},
                {'name': '자료구조', 'course': ['자료구조'], 'hours': 4},
                {'name': '공대 공통교과목', 'course': ['건설환경공학개론', '에너지자원공학개론', '산업공학개론', '화학생물공학개론', '기계공학개론', '재료공학개론'], 'hours': 3},
            ],
            [
                {'name': '소프트웨어 개발의 원리와 실제', 'course': ['소프트웨어 개발의 원리와 실제'], 'hours': 3},
                {'name': '시스템프로그래밍', 'course': ['시스템프로그래밍'], 'hours': 4},
            ],
            [
                {'name': '하드웨어시스템설계', 'course': ['하드웨어시스템설계'], 'hours': 3},
                {'name': '알고리즘', 'course': ['알고리즘'], 'hours': 3},
            ],
            [], [],
        ]
    if year <= 2014 and year >= 2011:
        return [
            [], [],
            [
                {'name': '컴퓨터프로그래밍', 'course': ['컴퓨터프로그래밍'], 'hours': 3},
                {'name': '이산수학', 'course': ['이산수학'], 'hours': 3},
                {'name': '논리설계', 'course': ['논리설계'], 'hours': 3},
                {'name': '논리설계실험', 'course': ['논리설계실험', '하드웨어시스템설계'], 'hours': 3},
            ],
            [
                {'name': '전기전자회로', 'course': ['전기전자회로'], 'hours': 3},
                {'name': '프로그래밍의 원리', 'course': ['프로그래밍의 원리'], 'hours': 3},
                {'name': '자료구조', 'course': ['자료구조'], 'hours': 3},
                {'name': '공대 공통교과목', 'course': ['건설환경공학개론', '에너지자원공학개론', '산업공학개론', '화학생물공학개론', '기계공학개론', '재료공학개론'], 'hours': 3},
            ],
            [
                {'name': '운영체제', 'course': ['운영체제'], 'hours': 3},
                {'name': '컴퓨터구조', 'course': ['컴퓨터구조'], 'hours': 3},
            ],
            [
                {'name': '프로그래밍언어', 'course': ['프로그래밍언어'], 'hours': 3},
                {'name': '알고리즘', 'course': ['알고리즘'], 'hours': 3},
            ],
            [], [],
        ]
    if year <= 2010:
        return [
            [], [],
            [
                {'name': '컴퓨터프로그래밍', 'course': ['컴퓨터프로그래밍'], 'hours': 3},
                {'name': '이산수학', 'course': ['이산수학'], 'hours': 3},
                {'name': '논리설계', 'course': ['논리설계'], 'hours': 3},
                {'name': '논리설계실험', 'course': ['논리설계실험', '하드웨어시스템설계'], 'hours': 3},
            ],
            [
                {'name': '전기전자회로', 'course': ['전기전자회로'], 'hours': 3},
                {'name': '프로그래밍의 원리', 'course': ['프로그래밍의 원리'], 'hours': 3},
                {'name': '자료구조', 'course': ['자료구조'], 'hours': 3},
            ],
            [
                {'name': '운영체제', 'course': ['운영체제'], 'hours': 3},
                {'name': '컴퓨터구조', 'course': ['컴퓨터구조'], 'hours': 3},
            ],
            [
                {'name': '프로그래밍언어', 'course': ['프로그래밍언어'], 'hours': 3},
                {'name': '알고리즘', 'course': ['알고리즘'], 'hours': 3},
            ],
            [], [],
        ]

def innerRule(year):
    if year >= 2015:
        return [
            {'name': '컴퓨터공학세미나/IT-리더십세미나', 'semester': 3, 'course': [['컴퓨터공학세미나', 'IT-리더십세미나']]},
            {'name': '창의적통합설계', 'semester': 6, 'course': [['프로젝트 1', '창의적통합설계1'], ['프로젝트 2', '창의적통합설계2']]},
        ]
    else:
        return [
            {'name': '컴퓨터공학세미나', 'semester': 5, 'course': [['컴퓨터공학세미나']]},
            {'name': 'IT-리더십세미나', 'semester': 6, 'course': [['IT-리더십세미나']]},
            {'name': '창의적통합설계', 'semester': 6, 'course': [['프로젝트 1', '창의적통합설계1'], ['프로젝트 2', '창의적통합설계2']]},
        ]

def AdjustCourse(course):
    semester = course['shtmDetaShtm']
    if semester == '여름학기':
        semester = '1학기'
    if semester == '겨울학기':
        semester = '2학기'
    if AdjustCourse.semester_name != course['schyy']+semester:
        AdjustCourse.semester += 1
        AdjustCourse.semester_name = course['schyy']+semester
    name = course['sbjtNm'].strip()
    return {
        'code': course['sbjtCd'],
        'name': name,
        'hours': course['acqPnt'],
        'course_type': course['cptnSubmattFgCdNm'],
        'semester': AdjustCourse.semester,
        'mandatory': 'false',
        'done': 'true',
        'act': 'false',
        'info': '',
    }

def flatRule(l):
    result = []
    for i in range(len(l)):
        for rule in l[i]:
            rule['semester'] = i
            result.append(rule)
    result.sort(key=lambda x: x['priority'] if 'priority' in x else 0, reverse=True)
    return result

def initGeneralCourses(year):
    creative = ['현대도시건축산책', '창조와 디자인', '테크놀러지와 예술: 전시예술공학', '소리의 과학과 악기제작 체험', '창의공학설계', '디지털아트공학', '공학도를 위한 창의적 사고']
    social = ['기술과 기업', '창업과 경제', '기술과 경제', '공학윤리와 리더십', '특허와 기술창업', '기술과 창업', '현대기술과 윤리적 사고', '공학기술의 역사', '공학인을 위한 경영']
    science = ['물리학 1', '물리학 2', '화학 1', '화학 2', '생물학 1', '생물학 2', '물리학', '화학', '생물학', '물리의 기본 1', '물리의 기본 2', '고급물리학 1', '고급물리학 2', '물리학실험', '물리학실험 1', '물리학실험 2', '화학실험 1', '화학실험 2', '화학실험', '생물학실험 1', '생물학실험 2', '생물학실험']
    advance_eng = ['고급영어: 영어권 문화의 이해', '고급영어학술발표', '고급영어: 영화', '고급영어: 시사토론', '고급영어학술작문', '고급영어: 문화와 사회', '고급영어: 연극을 통한 영어연습', '고급영어: 발표', '고급영어: 학술작문', '고급영어: 연극', '고급영어: 문학', '고급영어: 영상예술', '고급영어: 산문']
    eng2 = ['대학영어 2: 글쓰기', '대학영어 2: 말하기']
    if year >= 2015:
        return [
            [
                {'name': '[외국어]', 'subarea': '외국어', 'count': 1, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science, 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '글쓰기의 기초', 'course': ['글쓰기의 기초', '과학과 기술 글쓰기', '대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science, 'amount': 4, 'hours': 4, 'fullamount': 4},
            ],
            [
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '통계학', 'course': ['통계학'], 'hours': 3},
                {'name': '통계학실험', 'course': ['통계학실험'], 'hours': 1},
            ],
            [
                {'name': '[외국어]', 'subarea': '외국어', 'count': 1, 'hours': 2},
                {'name': '[학문의 세계]', 'area': '학문의 세계', 'hours': 3, 'amount': 3, 'fullamount': 3},
            ],
            [
                {'name': '[학문의 세계]', 'area': '학문의 세계', 'hours': 3, 'amount': 3, 'fullamount': 3},
            ],
            [
                {'name': '[사회성 교과목군]', 'course': social, 'subarea': '인간과 사회', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
            [
                {'name': '[창의성 교과목군]', 'course': creative, 'subarea': '문화와 예술', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
        ]
    if year == 2014:
        return [
            [
                {'name': '외국어', 'subarea': '외국어', 'count': 1, 'hours': 3},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science, 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '글쓰기의 기초', 'course': ['글쓰기의 기초', '과학과 기술 글쓰기', '대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science, 'amount': 4, 'hours': 4, 'fullamount': 4},
            ],
            [
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '통계학', 'course': ['통계학'], 'hours': 3},
                {'name': '통계학실험', 'course': ['통계학실험'], 'hours': 1},
            ],
            [
                {'name': '[외국어]', 'subarea': '외국어', 'count': 1, 'hours': 2},
                {'name': '[학문의 세계]', 'area': '학문의 세계', 'hours': 3, 'amount': 3, 'fullamount': 3},
            ],
            [
                {'name': '[학문의 세계]', 'area': '학문의 세계', 'hours': 3, 'amount': 3, 'fullamount': 3},
            ],
            [
                {'name': '[사회성 교과목군]', 'course': social, 'subarea': '인간과 사회', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
            [
                {'name': '[창의성 교과목군]', 'course': creative, 'subarea': '문화와 예술', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
        ]
    if year == 2013:
        return [
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '대학국어', 'course': ['대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
            ],
            [
                {'name': '[핵심교양-문학과예술]', 'subarea': '문학과 예술', 'hours': 3},
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '[핵심교양-역사와철학]', 'subarea': '역사와 철학', 'hours': 3},
            ],
            [
                {'name': '[핵심교양-사회와이념]', 'subarea': '사회와 이념', 'hours': 3},
            ],
            [
            ],
            [
                {'name': '[사회성 교과목군]', 'course': social, 'subarea': '인간과 사회', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
            [
                {'name': '[창의성 교과목군]', 'course': creative, 'subarea': '문화와 예술', 'hours': 3, 'priority': 1, 'amount': 3},
            ],
        ]
    if year <= 2012 and year >= 2011:
        return [
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '대학국어', 'course': ['대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
            ],
            [
                {'name': '[핵심교양-문학과예술]', 'subarea': '문학과 예술', 'hours': 3},
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '[핵심교양-역사와철학]', 'subarea': '역사와 철학', 'hours': 3},
            ],
            [
                {'name': '[핵심교양-사회와이념]', 'subarea': '사회와 이념', 'hours': 3},
            ],
            [
                {'name': '과학과 기술 글쓰기', 'course': ['과학과 기술 글쓰기'], 'hours': 3},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['과학기술과 사회', '경제학개론', '소비자와 시장', '경영학개론', '창업과 경제', '기술과 사회발전', '공학윤리와 리더십', '특허와 기술이전', '기술과 기업'], 'hours': 3, 'priority': 2},
            ],
            [
            ],
        ]
    if year == 2010:
        return [
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 개념 및 실습', 'course': ['컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '대학국어', 'course': ['대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
            ],
            [
                {'name': '[핵심교양-문학과예술]', 'subarea': '문학과 예술', 'hours': 3},
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '[핵심교양-역사와철학]', 'subarea': '역사와 철학', 'hours': 3},
            ],
            [
                {'name': '[핵심교양-사회와이념]', 'subarea': '사회와 이념', 'hours': 3},
            ],
            [
                {'name': '과학과 기술 글쓰기', 'course': ['과학과 기술 글쓰기'], 'hours': 3},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['경제학개론', '소비자와 시장', '경영학개론', '창업과 경제'], 'hours': 3, 'priority': 1},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['정보와 산업기술의 이해', '컴퓨터와 마음', '두뇌의 이해', '공학윤리와 리더십', '특허와 기술이전', '기술과 기업'], 'hours': 3},
            ],
        ]
    if year == 2009:
        return [
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 기초', 'course': ['컴퓨터의 기초', '컴퓨터원리', '컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '대학국어', 'course': ['대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
            ],
            [
                {'name': '[핵심교양-문학과예술]', 'subarea': '문학과 예술', 'hours': 3},
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '[영어]', 'course': ['대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '[핵심교양-역사와철학]', 'subarea': '역사와 철학', 'hours': 3},
            ],
            [
                {'name': '[핵심교양-사회와이념]', 'subarea': '사회와 이념', 'hours': 3},
            ],
            [
                {'name': '과학과 기술 글쓰기', 'course': ['과학과 기술 글쓰기'], 'hours': 3},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['경제학개론', '소비자와 시장', '경영학개론', '창업과 경제'], 'hours': 3, 'priority': 1},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['정보와 산업기술의 이해', '컴퓨터와 마음', '두뇌의 이해', '공학윤리와 리더십', '특허와 기술이전', '기술과 기업'], 'hours': 3},
            ],
        ]
    else:
        return [
            [
                {'name': '[영어]', 'course': ['대학영어', '대학영어 1']+eng2+advance_eng, 'hours': 2},
                {'name': '수학 및 연습1', 'course': ['수학 및 연습 1', '고급수학 및 연습 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
                {'name': '컴퓨터의 기초', 'course': ['컴퓨터의 기초', '컴퓨터원리', '컴퓨터의 개념 및 실습'], 'hours': 3}
            ],
            [
                {'name': '대학국어', 'course': ['대학국어'], 'hours': 3},
                {'name': '수학 및 연습2', 'course': ['수학 및 연습 2', '고급수학 및 연습 2'], 'hours': 3},
                {'name': '공학수학 1', 'course': ['공학수학 1'], 'hours': 3},
                {'name': '[과학적 사고와 실험]', 'course': science + ['통계학', '통계학실험'], 'amount': 8, 'hours': 8, 'fullamount': 8},
            ],
            [
                {'name': '[핵심교양-문학과예술]', 'subarea': '문학과 예술', 'hours': 3},
                {'name': '공학수학 2', 'course': ['공학수학 2'], 'hours': 3},
            ],
            [
                {'name': '[핵심교양-역사와철학]', 'subarea': '역사와 철학', 'hours': 3},
            ],
            [
                {'name': '[핵심교양-사회와이념]', 'subarea': '사회와 이념', 'hours': 3},
            ],
            [
                {'name': '과학과 기술 글쓰기', 'course': ['과학과 기술 글쓰기'], 'hours': 3},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['경제학개론', '소비자와 시장', '경영학개론', '창업과 경제'], 'hours': 3, 'priority': 1},
            ],
            [
                {'name': '[공학소양관련]', 'course': ['정보와 산업기술의 이해', '컴퓨터와 마음', '두뇌의 이해', '공학윤리와 리더십', '특허와 기술이전', '기술과 기업'], 'hours': 3},
            ],
        ]

def majorAllSum(year):
    if year >= 2011:
        return 63
    else:
        return 60

def cseCrawl():
    url = 'http://cse.snu.ac.kr/undergraduate/courses'
    r = requests.get(url)
    soup = bs(r.text, 'html5lib')
    table = soup.table
    result = []
    for course in table.tbody.find_all('tr'):
        extract = []
        for td in course.find_all('td'):
            content = td.string
            if content != None:
                content = content.strip()
            if td.a != None:
                content = td.a.string.strip()
            extract.append(content)
        result.append({'code': extract[1], 'name': extract[2], 'hours': int(extract[3]), 'year': int(extract[4][:1])})
    return result

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
    tmp = [course for course in courses['GRD_SCOR401'] if course['mrksGrdCd'] in ['A+', 'A0', 'A-', 'B+', 'B0', 'B-', 'C+', 'C0', 'C-', 'D+', 'D0', 'D-', 'S']]
    tmp.sort(key=lambda x: (int(x['schyy']) * 10 + (0 if x['shtmDetaShtm'] in ['1학기', '여름학기'] else 1)))
    result = [AdjustCourse(course) for course in tmp]
    total_semester = AdjustCourse.semester + 1
    dept_json = br.post('https://shine.snu.ac.kr/uni/uni/scor/mrtr/findTabCumlMrksYyShtmClsfTtInq01List2.action',
            params={'cscLocale':'ko_KR','strPgmCd':'S030302'}, headers=headers,
            json={"SUN":{"strSchyy":"2016","strShtmFg":"U000200001","strDetaShtmFg":"U000300001","strBdegrSystemFg":"U000100001","strFlag":"all"}}).text
    user_json = br.post('https://shine.snu.ac.kr/com/com/sstm/logn/findUserInfo.action', headers=headers,
            json={"findUsers":{"rType":"3tier","logType":"systemConn","chgUserYn":"N","chgBfUser":"","chgAfUser":""}}).text
    name = json.loads(user_json)['userInfos'][0]['USERNM']
    dept = json.loads(user_json)['userInfos'][0]['DEPARTMENTKORNM']
    stuno = json.loads(user_json)['userInfos'][0]['USERID']

    majorRules = initMajorCourses(int(stuno[:4]))
    majors = [[] for _ in range(max(8, total_semester))]
    majorCourses = [course for course in result if course['course_type'] in ['전필', '전선']]

    for semester in range(len(majorRules)):
        toRemove = []
        for rule in majorRules[semester]:
            for course in majorCourses:
                if course['name'] in rule['course']:
                    majorCourses.remove(course)
                    course['mandatory'] = 'true'
                    course['done'] = 'true'
                    majors[course['semester']].append(course)
                    toRemove.append(rule)
                    break
        for removeRule in toRemove:
            majorRules[semester].remove(removeRule)
    for semester in range(len(majorRules)):
        for rule in majorRules[semester]:
            done = False
            for course in result:
                if course['name'] in rule['course']:
                    majors[semester].append({
                        'name': course['name'],
                        'mandatory': '1',
                        'done': 'true',
                        'act': 'true',
                        'hours': course['hours'],
                        'info': '전필로 전환이 필요합니다'
                        })
                    done = True
                    break
            if not done:
                majors[semester].append({
                    'name': rule['name'],
                    'mandatory': 'true',
                    'done': 'false',
                    'act': 'true',
                    'hours': rule['hours'],
                    'info': '\\n'.join(rule['course'])
                    })

    electiveScore = 0
    majorSum = 0
    majorDoneSum = 0
    for semester in majors:
        for course in semester:
            if course['mandatory'] == 'true':
                majorSum += course['hours']
                if course['done'] == 'true':
                    majorDoneSum += course['hours']
    for rule in innerRule(int(stuno[:4])):
        removeSubrule = []
        done = False
        for subrule in rule['course']:
            toRemove = []
            for course in majorCourses:
                if course['name'] in subrule:
                    course['done'] = 'true'
                    course['mandatory'] = 'true'
                    rule['act'] = 'false'
                    rule['info'] = ''
                    majors[course['semester']].append(course)
                    toRemove.append(course)
                    removeSubrule.append(subrule)
                    done = True
                    break
            for remove in toRemove:
                majorCourses.remove(remove)
        for remove in removeSubrule:
            rule['course'].remove(remove)
        if not done:
            rule['done'] = 'false'
            rule['mandatory'] = 'true'
            rule['act'] = 'true'
            rule['info'] = '\\n'.join([j for i in rule['course'] for j in i])
            majors[rule['semester']].append(rule)
    for course in majorCourses:
        if course['course_type'] == '전필':
            course['mandatory'] = '1'
            course['done'] = 'true'
            course['act'] = 'true'
            course['info'] = '전선으로 전환이 필요합니다'
            majors[course['semester']].append(course)
        else:
            electiveScore += course['hours']
            course['mandatory'] = 'false'
            course['done'] = 'true'
            course['act'] = 'false'
            course['info'] = ''
            majors[course['semester']].append(course)

    global ELECTIVES
    electives = [[] for _ in range(max(8, total_semester))]
    majorCourses = initMajorCourses(int(stuno[:4]))
    for course in ELECTIVES:
        if Course.objects.filter(name=course['name']).count() == 0:
            continue
        if course['name'] in [course['name'] for course in result]:
            continue
        isMajor = False
        for semester in majorCourses:
            for major in semester:
                for replaceableCourse in major['course']:
                    if course['name'] == replaceableCourse:
                        isMajor = True
        if isMajor:
            continue
        if Course.objects.filter(name=course['name'], semester='1').count() > Course.objects.filter(name=course['name'], semester='2').count():
            electives[course['year'] * 2 - 2].append(course)
        else:
            electives[course['year'] * 2 - 1].append(course)
    for i in range(len(majors)):
        if electives[i]:
            majors[i].append({
                'code': '',
                'name': '전선',
                'hours': 0,
                'mandatory': 'false',
                'done': 'false',
                'act': 'true',
                'info': '\\n'.join([course['name'] for course in electives[i]])
                })
    # 교양
    generalCourses = flatRule(initGeneralCourses(int(stuno[:4])))
    generals = [[] for _ in range(max(8, total_semester))]
    generalsDone = [course for course in result if course['course_type'] == '교양']
    generalRule = []
    for rule in generalCourses:
        done = False
        if 'area' in rule:
            areaList = [course.code for course in Course.objects.filter(area=rule['area'])]
            toRemove = []
            for course in generalsDone:
                if course['code'] in areaList:
                    toRemove.append(course)
                    rule['hours'] -= course['hours']
                    course['mandatory'] = 'true'
                    course['act'] = 'true';
                    course['info'] = rule['area'];
                    generals[course['semester']].append(course)
                if rule['hours'] <= 0:
                    done = True
                    break
            for remove in toRemove:
                generalsDone.remove(remove)
        if 'subarea' in rule and not done:
            toRemove = []
            if 'amount' in rule:
                toRemove = []
                for course in generalsDone:
                    if Course.objects.filter(name=course['name'], subarea=rule['subarea']).count() > 0:
                        rule['amount'] -= course['hours']
                        course['mandatory'] = 'true'
                        course['act'] = 'true';
                        course['info'] = rule['subarea'];
                        toRemove.append(course)
                        generals[course['semester']].append(course)
                    if rule['amount'] <= 0:
                        for another in generalCourses:
                            if another != rule and another['name'] == rule['name']:
                                another['amount'] += rule['amount']
                                break
                        done = True
                        break
                for remove in toRemove:
                    generalsDone.remove(remove)
            else:
                for course in generalsDone:
                    if Course.objects.filter(subarea=rule['subarea'], name=course['name']).count() > 0:
                        done = True
                        if 'count' in rule:
                            rule['count'] -= 1
                        if 'hours' in rule:
                            rule['hours'] -= course['hours']
                        course['mandatory'] = 'true'
                        course['act'] = 'true';
                        course['info'] = rule['subarea'];
                        toRemove.append(course)
                        generals[course['semester']].append(course)
                    if 'count' in rule:
                        if rule['count'] <= 0:
                            done = True
                            break
                    if 'hours' in rule:
                        if rule['hours'] <= 0:
                            done = True
                            break
                for remove in toRemove:
                    generalsDone.remove(remove)
        if 'course' in rule and not done:
            if 'amount' in rule:
                toRemove = []
                for course in generalsDone:
                    if course['name'] in rule['course']:
                        rule['course'].remove(course['name'])
                        course['act'] = 'false';
                        course['info'] = '';
                        rule['amount'] -= course['hours']
                        course['mandatory'] = 'true'
                        toRemove.append(course)
                        generals[course['semester']].append(course)
                    if rule['amount'] <= 0:
                        for another in generalCourses:
                            if another != rule and another['name'] == rule['name']:
                                another['amount'] += rule['amount']
                                break
                        done = True
                        break
                for remove in toRemove:
                    generalsDone.remove(remove)
            elif 'hours' in rule:
                toRemove = []
                for course in generalsDone:
                    if course['name'] in rule['course']:
                        rule['course'].remove(course['name'])
                        rule['hours'] -= course['hours']
                        course['mandatory'] = 'true'
                        course['act'] = 'false';
                        course['info'] = '';
                        toRemove.append(course)
                        generals[course['semester']].append(course)
                    if rule['hours'] <= 0:
                        done = True
                        break
                for remove in toRemove:
                    generalsDone.remove(remove)
            else:
                toRemove = []
                for course in generalsDone:
                    if course['name'] in rule['course']:
                        rule['course'].remove(course['name'])
                        course['mandatory'] = 'true'
                        course['act'] = 'false';
                        course['info'] = '';
                        toRemove.append(course)
                        generals[course['semester']].append(course)
                        done = True
                        break
                for remove in toRemove:
                    generalsDone.remove(remove)
        if not done:
            generalRule.append(rule)

    for rule in generalRule:
        if rule['name'] == '[영어]':
            advance_eng = ['고급영어: 영어권 문화의 이해', '고급영어학술발표', '고급영어: 영화', '고급영어: 시사토론', '고급영어학술작문', '고급영어: 문화와 사회', '고급영어: 연극을 통한 영어연습', '고급영어: 발표', '고급영어: 학술작문', '고급영어: 연극', '고급영어: 문학', '고급영어: 영상예술', '고급영어: 산문']
            done = False
            for course in result:
                if course['name'] in advance_eng:
                    done = True
                    break
            if done:
                continue
        rule['mandatory'] = 'true'
        rule['done'] = 'false'
        rule['act'] = 'true';
        rule['info'] = '';
        if 'area' in rule:
            rule['info'] += '\\n'.join(list(set([course.name for course in Course.objects.filter(area=rule['area'])])))
        if 'subarea' in rule:
            rule['info'] += '\\n'.join(list(set([course.name for course in Course.objects.filter(subarea=rule['subarea'])])))
        if 'course' in rule:
            rule['info'] += '\\n'.join(rule['course'])
        if 'amount' in rule:
            rule['name'] += ' (' + str(rule['amount']) + ')'
        generals[rule['semester']].append(rule)
    for course in generalsDone:
        course['mandatory'] = 'false'
        course['done'] = 'true'
        course['act'] = 'false';
        course['info'] = '';
        generals[course['semester']].append(course)

    generalSum = 0
    generalDoneSum = 0
    for semester in generals:
        for course in semester:
            if course['mandatory'] == 'true':
                if 'amount' in course:
                    generalSum += course['amount']
                else:
                    generalSum += course['hours']
                if course['done'] == 'true':
                    generalDoneSum += course['hours']

    score = sum([course['hours'] for course in result])
    return {'courses': result, 'dept': dept, 'stuno': stuno, 'majorCourses': majors, 'score': score, 'name': name, 'generals': generals, 'majorSum': majorSum, 'majorDoneSum': majorDoneSum, 'electiveDoneSum': electiveScore, 'electiveSum': majorAllSum(int(stuno[:4])) - majorSum, 'electives': electives, 'generalSum': generalSum, 'generalDoneSum': generalDoneSum}

def login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html', {'alert': request.session.get('alert', False)})
    elif request.method == 'POST':
        data = QueryDict(request.body)
        mysnu_username = data['username']
        mysnu_password = data['password']
        result = dict()
        try:
            result = crawlCourse(mysnu_username, mysnu_password)
        except Exception:
            request.session['alert'] = True
            return redirect('login')
        request.session['result'] = result
        request.session.set_expiry(3600)
        return redirect('courses')

def courses(request):
    if request.session.get('result', False):
        return render(request, 'core/result.html', request.session['result'])
    return redirect('login')

def logout(request):
    request.session.flush()
    return redirect('login')

ELECTIVES = cseCrawl()
