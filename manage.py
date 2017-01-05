#!/usr/bin/env python
# Copyright (c) 2016, Shin DongJin. See the LICENSE file
# at the top-level directory of this distribution and at
# https://github.com/LastOne817/graduate/blob/master/LICENSE
#
# Licensed under the MIT license <http://opensource.org/licenses/MIT>.
# This file may not be copied, modified, or distributed except according
# to those terms.

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graduate.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
