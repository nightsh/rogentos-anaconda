#
# timezone.py - timezone install data
#
# Copyright (C) 2001  Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import shutil
import iutil
import os
from flags import flags

import logging
log = logging.getLogger("anaconda")

class Timezone:
    def writeKS(self, f):
        f.write("timezone")
        if self.utc:
            f.write(" --utc")
        f.write(" %s\n" % self.tz)

    def write(self, instPath):

        fromFile = "/usr/share/zoneinfo/" + self.tz
        tzfile = instPath + "/etc/localtime"

        if os.path.isdir(instPath+"/etc"):

            try:
                if os.path.lexists(tzfile):
                    os.remove(tzfile)
                os.symlink(fromFile, tzfile)
            except OSError, e:
                log.error("Error copying timezone (from %s): %s" % (
                    fromFile, e,))

            f = open(instPath + "/etc/timezone", "w")
            f.write(self.tz)
            f.flush()
            f.close()

        # set clock config
        clock_conf = instPath+"/etc/conf.d/hwclock"
        if not os.path.isfile(clock_conf):
            log.info("Cannot find "+clock_conf)
        else:
            f = open(clock_conf,"r")
            olddata = [x.strip() for x in f.readlines()]
            f.close()
            newdata = []
            for item in olddata:
                if item.startswith("clock="):
                    if self.utc:
                        item = "clock=\"UTC\""
                    else:
                        item = "clock=\"local\""
                newdata.append(item)
            f = open(instPath+"/etc/conf.d/hwclock", "w")
            for item in newdata:
                f.write(item+"\n")
            f.flush()
            f.close()

    def getTimezoneInfo(self):
        return (self.tz, self.utc)

    def setTimezoneInfo(self, timezone, asUtc = 0):
        self.tz = timezone
        self.utc = asUtc

    def __init__(self):
        self.tz = "America/New_York"
        self.utc = 0
