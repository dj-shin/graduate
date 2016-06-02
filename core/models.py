from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Area(models.Model):   # 영역
    name = models.CharField(max_length=40)

    def __str__(self):
        return '<영역 : %s>' % self.name

class Course(models.Model): # 과목
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    hours = models.PositiveSmallIntegerField()
    
    MANDATORY = 'MA'    # 전필
    ELECTIVE = 'EL'     # 전선
    COURSE_TYPE_CHOICES = (
        (MANDATORY, '전공 필수'),
        (ELECTIVE, '전공 선택'),
    )
    course_type = models.CharField(max_length=2, choices=COURSE_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return '<과목 : %s>' % self.name

    def toJSON(self):
        result = {}
        result['code'] = self.code
        result['name'] = self.name
        if self.area:
            result['area'] = self.area
        result['hours'] = self.hours
        if self.course_type:
            result['course_type'] = self.course_type
        return result

class CourseAcquired(models.Model):
    course = None
    acquired_type = None
    major_type = None

    def __init__(self, course_id, acquired_type='교양', major_type=''):
        try:
            self.course = Course.objects.get(pk=course_id)
        except ObjectDoesNotExist:
            self.course = Course.objects.get(name=course_id)
        self.acquired_type = acquired_type
        self.major_type = major_type

    def __str__(self):
        return '<이수과목 : %s>' % self.course.name

class Rule(models.Model):   # 규정
    dept = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    MAJOR = 'MA'    # 주전공
    MINOR = 'MI'    # 부전공
    DOUBLE_MAJOR = 'DM' # 복수전공
    MAJOR_TYPE_CHOICES = (
        (MAJOR, '주전공'),
        (MINOR, '부전공'),
        (DOUBLE_MAJOR, '복수전공'),
    )
    major_type = models.CharField(max_length=2, choices=MAJOR_TYPE_CHOICES, default=MAJOR)

    AREA = 'AR'     # 영역
    COURSE = 'CO'   # 과목
    RULE_TYPE_CHOICES = (
        (AREA, '영역'),
        (COURSE, '과목'),
    )
    rule_type = models.CharField(max_length=2, choices=RULE_TYPE_CHOICES)

    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField(Course, symmetrical=False, blank=True)

    HOURS = 'HO'    # 학점수
    COUNT = 'CO'    # 과목수
    VALUE_TYPE_CHOICES = (
        (HOURS, '학점수'),
        (COUNT, '과목수'),
    )
    value_type = models.CharField(max_length=2, choices=VALUE_TYPE_CHOICES)

    value = models.PositiveSmallIntegerField()

    scope_from = models.PositiveSmallIntegerField(null=True, blank=True)
    scope_to = models.PositiveSmallIntegerField(null=True, blank=True)

    def toJSON(self):
        result = {}
        result['dept'] = self.dept.name
        result['description'] = self.description
        result['major_type'] = self.major_type
        if self.rule_type:
            result['rule_type'] = self.rule_type
        if self.area:
            result['area'] = self.area
        if self.courses.all() != []:
            result['courses'] = [course.toJSON() for course in self.courses.all()]
        result['value_type'] = self.value_type
        result['value'] = self.value
        if self.scope_from:
            result['scope_from'] = self.scope_from
        if self.scope_to:
            result['scope_to'] = self.scope_to
        return result

    def __str__(self):
        ruleTypeDict = {Rule.AREA: '영역', Rule.COURSE: '과목'}
        valueTypeDict = {Rule.HOURS: '학점', Rule.COUNT: '과목'}
        content = None
        if self.rule_type == Rule.AREA:
            content = self.area.name
        else:
            content = [course.name for course in self.courses.all()]
        if not content:
            content = ''
        return '<%s 규정 : %s 중 %s%s 이상 (%s - %s)>' % (
                ruleTypeDict[self.rule_type],
                content,
                self.value,
                valueTypeDict[self.value_type],
                self.scope_from,
                self.scope_to)

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return '<학부 : %s>' % self.name
