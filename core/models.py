from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100, null=False)
    hours = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=40)
    subarea = models.CharField(max_length=40)
    semester = models.CharField(max_length=10)

    def toJSON(self):
        return {
            'code': self.code,
            'name': self.name,
            'hours': self.hours,
            'area': self.area,
            'subarea': self.subarea,
            'year': self.year,
            'semester': self.semester,
        }

    def __str__(self):
        return '%s(%s)' % (self.name, self.code)
