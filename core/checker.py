from .models import Area, Course, CourseAcquired, Rule, Department


def counter(course, rule):
    if rule.value_type == Rule.HOURS:
        return course.hours
    elif rule.value_type == Rule.COUNT:
        return 1
    else:
        raise Exception('Wrong value type of rule %s' % str(rule))

def ApplyRule(rules, coursesAcquired):
    violatedRules = []
    for rule in rules:
        if rule.rule_type == Rule.AREA:
            area_sum = sum([counter(ac, rule) for ac in coursesAcquired if ac.course.area == rule.area])
            if area_sum < rule.value:
                violatedRules.append(rule)
        elif rule.rule_type == Rule.COURSE:
            course_sum = sum([counter(ac, rule) for ac in coursesAcquired if ac.course in rule.courses.all()])
            if course_sum < rule.value:
                violatedRules.append(rule)
    return violatedRules
