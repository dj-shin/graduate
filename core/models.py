from django.db import models


class Area(models.Model):   # 영역
    name = models.CharField(max_length=40)

    def __str__(self):
        return '<영역 : %s>' % self.name

class Course(models.Model): # 과목
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True)
    hours = models.PositiveSmallIntegerField()
    
    MANDATORY = 'MA'    # 전필
    ELECTIVE = 'EL'     # 전선
    COURSE_TYPE_CHOICES = (
        (MANDATORY, '전공 필수'),
        (ELECTIVE, '전공 선택'),
    )
    course_type = models.CharField(max_length=2, choices=COURSE_TYPE_CHOICES, null=True)

    def __str__(self):
        return '<과목 : %s>' % self.name

class CourseAcquired(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    CULTURE = 'CU'      # 교양
    MANDATORY = 'MA'    # 전필
    ELECTIVE = 'EL'     # 전선
    N_ELECTIVE = 'NL'   # 일선
    ACQUIRED_TYPE_CHOICES = (
        (CULTURE, '교양'),
        (MANDATORY, '전공 필수'),
        (ELECTIVE, '전공 선택'),
        (N_ELECTIVE, '일반 선택'),
    )
    acquired_type = models.CharField(max_length=2, choices=ACQUIRED_TYPE_CHOICES, null=True)
    MAJOR = 'MA'    # 주전공
    MINOR = 'MI'    # 부전공
    DOUBLE_MAJOR = 'DM' # 복수전공
    MAJOR_TYPE_CHOICES = (
        (MAJOR, '주전공'),
        (MINOR, '부전공'),
        (DOUBLE_MAJOR, '복수전공'),
    )
    major_type = models.CharField(max_length=2, choices=MAJOR_TYPE_CHOICES, null=True)

    def __str__(self):
        return '<이수과목 : %s>' % self.course.name

class Rule(models.Model):   # 규정
    dept = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
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
    CUSTOM = 'CU'   # 임의
    RULE_TYPE_CHOICES = (
        (AREA, '영역'),
        (COURSE, '과목'),
        (CUSTOM, '임의'),
    )
    rule_type = models.CharField(max_length=2, choices=RULE_TYPE_CHOICES)

    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Course)

    HOURS = 'HO'    # 학점수
    COUNT = 'CO'    # 과목수
    VALUE_TYPE_CHOICES = (
        (HOURS, '학점수'),
        (COUNT, '과목수'),
    )
    value_type = models.CharField(max_length=2, choices=VALUE_TYPE_CHOICES)

    value = models.PositiveSmallIntegerField()

    def __str__(self):
        ruleTypeDict = {AREA: '영역', COURSE: '과목', CUSTOM: '임의'}
        valueTypeDict = {HOURS: '학점', COUNT: '과목'}
        content = None
        if self.rule_type == AREA:
            content = self.area
        else:
            content = self.courses
        return '<%s 규정 : %s (%s 중 %d%s 이상)>' % (namedict[self.rule_type], str(content), self.value, valueTypeDict[self.value_type])

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return '<학부 : %s>' % self.name
