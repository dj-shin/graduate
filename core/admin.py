from django.contrib import admin
from .models import Area, Course, CourseAcquired, Rule, Department


admin.site.register([Area, Course, CourseAcquired, Rule, Department])
