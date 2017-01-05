# Copyright (c) 2016, Shin DongJin. See the LICENSE file
# at the top-level directory of this distribution and at
# https://github.com/LastOne817/graduate/blob/master/LICENSE
#
# Licensed under the MIT license <http://opensource.org/licenses/MIT>.
# This file may not be copied, modified, or distributed except according
# to those terms.

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.courses, name='courses'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
