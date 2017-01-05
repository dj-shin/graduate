# Copyright (c) 2016, Shin DongJin. See the LICENSE file
# at the top-level directory of this distribution and at
# https://github.com/LastOne817/graduate/blob/master/LICENSE
#
# Licensed under the MIT license <http://opensource.org/licenses/MIT>.
# This file may not be copied, modified, or distributed except according
# to those terms.

from django.test import TestCase
from core.models import Area, Course, CourseAcquired, Rule, Department
from core.checker import ApplyRule
from core.crawler import cseCrawl


class SuccessTestCase(TestCase):
    def test_basic_success(self):
        success = [
            CourseAcquired('이산수학'),
            CourseAcquired('전기전자회로'),
            CourseAcquired('프로그래밍의 원리'),
            CourseAcquired('운영체제'),
            CourseAcquired('컴퓨터구조'),
            CourseAcquired('프로그래밍언어'),
            CourseAcquired('알고리즘'),
            CourseAcquired('컴퓨터프로그래밍'),
            CourseAcquired('논리설계'),
            CourseAcquired('자료구조')
        ]
        cseCrawl()
        print(Course.objects.all())
        result = ApplyRule(Rule.objects.all(), success)
        self.assertEqual(result, [])
