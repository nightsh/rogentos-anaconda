#
# netconfig_text.py: Configure a network interface now.
#
# Copyright (C) 2008  Red Hat, Inc.
# All rights reserved.
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
# Author(s): Chris Lumens <clumens@redhat.com>
#            David Cantrell <dcantrell@redhat.com>
#


import isys
import network
from snack import *
from constants_text import *

import gettext
_ = lambda x: gettext.ldgettext("anaconda", x)

class NetworkConfiguratorText:
    def _handleIPError(self, field, errmsg):
        self.anaconda.intf.messageWindow(_("Error With Data"),
                                         _("An error occurred converting the "
                                           "value entered for \"%s\":\n%s") % (field, errmsg))

    def _handleIPMissing(self, field):
        self.anaconda.intf.messageWindow(_("Error With Data"),
                                         _("A value is required for the field %s") % field)

    def _dhcpToggled(self, *args):
        if self.dhcpCheckbox.selected():
            self.ipv4Address.setFlags(FLAG_DISABLED, FLAGS_SET)
            self.ipv4Netmask.setFlags(FLAG_DISABLED, FLAGS_SET)
            self.ipv6Address.setFlags(FLAG_DISABLED, FLAGS_SET)
            self.ipv6Netmask.setFlags(FLAG_DISABLED, FLAGS_SET)
            self.gatewayEntry.setFlags(FLAG_DISABLED, FLAGS_SET)
            self.nameserverEntry.setFlags(FLAG_DISABLED, FLAGS_SET)
        else:
            self.ipv4Address.setFlags(FLAG_DISABLED, int(self.ipv4Checkbox.selected()))
            self.ipv4Netmask.setFlags(FLAG_DISABLED, int(self.ipv4Checkbox.selected()))
            self.ipv6Address.setFlags(FLAG_DISABLED, int(self.ipv6Checkbox.selected()))
            self.ipv6Netmask.setFlags(FLAG_DISABLED, int(self.ipv6Checkbox.selected()))
            self.gatewayEntry.setFlags(FLAG_DISABLED, FLAGS_RESET)
            self.nameserverEntry.setFlags(FLAG_DISABLED, FLAGS_RESET)

    def _ipv4Toggled(self, *args):
        if self.dhcpCheckbox.selected():
            return

        flag = FLAGS_RESET
        if not self.ipv4Checkbox.selected():
            flag = FLAGS_SET

        self.ipv4Address.setFlags(FLAG_DISABLED, flag)
        self.ipv4Netmask.setFlags(FLAG_DISABLED, flag)

    def _ipv6Toggled(self, *args):
        if self.dhcpCheckbox.selected():
            return

        flag = FLAGS_RESET
        if not self.ipv6Checkbox.selected():
            flag = FLAGS_SET

        self.ipv6Address.setFlags(FLAG_DISABLED, flag)
        self.ipv6Netmask.setFlags(FLAG_DISABLED, flag)

    def __init__(self, screen, anaconda):
        self.screen = screen
        self.anaconda = anaconda

    def run(self):
        grid = GridFormHelp(self.screen, _("Enable network interface"), "netconfig",
                            1, 9)

        tb = TextboxReflowed(60, _("This requires that you have an active "
                                   "network connection during the installation "
                                   "process.  Please configure a network "
                                   "interface."))
        grid.add(tb, 0, 0, anchorLeft = 1, padding = (0, 0, 0, 1))

        self.interfaceList = CheckboxTree(height=3, scroll=1)

        netdevs = self.anaconda.id.network.available()
        devs = netdevs.keys()
        devs.sort()
        for dev in devs:
            desc = netdevs[dev].get("desc")
            if desc:
                desc = "%s - %s" % (dev, desc)
            else:
                desc = dev

            self.interfaceList.append(desc)

        grid.add(self.interfaceList, 0, 1, padding = (0, 0, 0, 1))

        self.dhcpCheckbox = Checkbox(_("Use dynamic IP configuration (DHCP)"), 1)
        grid.add(self.dhcpCheckbox, 0, 2, anchorLeft = 1)

        self.ipv4Checkbox = Checkbox(_("Enable IPv4 support"), 1)
        grid.add(self.ipv4Checkbox, 0, 3, anchorLeft = 1)

        self.ipv6Checkbox = Checkbox(_("Enable IPv6 support"), 0)
        grid.add(self.ipv6Checkbox, 0, 4, anchorLeft = 1, padding = (0, 0, 0, 1))

        ipv4Grid = Grid(4, 1)
        ipv4Grid.setField(Label(_("IPv4 Address:")), 0, 0, padding = (0, 0, 1, 0))
        self.ipv4Address = Entry(20, scroll=1)
        ipv4Grid.setField(self.ipv4Address, 1, 0)
        ipv4Grid.setField(Label("/"), 2, 0)
        self.ipv4Netmask = Entry(20, scroll=0)
        ipv4Grid.setField(self.ipv4Netmask, 3, 0)

        grid.add(ipv4Grid, 0, 5, anchorLeft = 1)

        ipv6Grid = Grid(4, 1)
        ipv6Grid.setField(Label(_("IPv6 Address:")), 0, 0, padding = (0, 0, 1, 0))
        self.ipv6Address = Entry(20, scroll=1)
        ipv6Grid.setField(self.ipv6Address, 1, 0)
        ipv6Grid.setField(Label("/"), 2, 0)
        self.ipv6Netmask = Entry(20, scroll=0)
        ipv6Grid.setField(self.ipv6Netmask, 3, 0)

        grid.add(ipv6Grid, 0, 6, anchorLeft = 1)

        extraGrid = Grid(4, 1)
        extraGrid.setField(Label(_("Gateway:")), 0, 0, padding = (0, 0, 1, 0))
        self.gatewayEntry = Entry(20, scroll=1)
        extraGrid.setField(self.gatewayEntry, 1, 0, padding = (0, 0, 2, 0))
        extraGrid.setField(Label(_("Nameserver:")), 2, 0, padding = (0, 0, 1, 0))
        self.nameserverEntry = Entry(20, scroll=1)
        extraGrid.setField(self.nameserverEntry, 3, 0)

        grid.add(extraGrid, 0, 7, anchorLeft = 1)

        buttons = ButtonBar(self.screen, [TEXT_OK_BUTTON, TEXT_BACK_BUTTON] )
        grid.add(buttons, 0, 8, anchorLeft = 1, growx = 1)

        self.dhcpCheckbox.setCallback(self._dhcpToggled)
        self.ipv4Checkbox.setCallback(self._ipv4Toggled)
        self.ipv6Checkbox.setCallback(self._ipv6Toggled)

        # Call these functions to set initial UI state.
        self._ipv4Toggled()
        self._ipv6Toggled()

        while True:
            result = grid.run()

            if result == TEXT_BACK_BUTTON:
                break

            cur = self.interfaceList.getCurrent()
            if cur:
                cur = cur.split()[0]
            else:
                self.anaconda.intf.messageWindow(_("Missing Device"),
                                                 _("You must select a network device"))
                continue

            netdev = self.anaconda.id.network.available()[cur]
            netdev.set(("useipv4", True))

            if self.dhcpCheckbox.selected():
                netdev.set(("bootproto", "dhcp"))
                w = self.anaconda.intf.waitWindow(_("Dynamic IP"),
                        _("Sending request for IP information "
                          "for %s...") % netdev.get("device"))
                ns = isys.dhcpNetDevice(netdev)
                w.pop()

                if ns is None:
                    break
                else:
                    f = open("/etc/resolv.conf", "w")
                    f.write("nameserver %s\n" % ns)
                    f.close()
                    isys.resetResolv()
            else:
                ipv4addr = self.ipv4Address.value()
                ipv4nm = self.ipv4Netmask.value()
                gateway = self.gatewayEntry.value()
                ns = self.nameserverEntry.value()

                try:
                    network.sanityCheckIPString(ipv4addr)
                    netdev.set(("ipaddr", ipv4addr))
                except network.IPMissing, msg:
                    self._handleIPMissing(_("IP Address"))
                    continue
                except network.IPError, msg:
                    self._handleIPError(_("IP Address"), msg)
                    continue

                if ipv4nm.find('.') == -1:
                    # user provided a CIDR prefix
                    try:
                        if int(ipv4nm) > 32 or int(ipv4nm) < 0:
                            msg = _("IPv4 CIDR prefix must be between 0 and 32.")
                            self._handleIPError(_("IPv4 Network Mask"), msg)
                            continue
                        else:
                            ipv4nm = isys.prefix2netmask(int(ipv4nm))
                            netdev.set(("netmask", ipv4nm))
                    except:
                        self._handleIPMissing(_("IPv4 Network Mask"))
                        continue
                else:
                    # user provided a dotted-quad netmask
                    try:
                        network.sanityCheckIPString(ipv4nm)
                        netdev.set(("netmask", ipv4nm))
                    except network.IPMissing, msg:
                        self._handleIPMissing(_("IPv4 Network Mask"))
                        continue
                    except network.IPError, msg:
                        self._handleIPError(_("IPv4 Network Mask "), msg)
                        continue

                try:
                    if gateway:
                        network.sanityCheckIPString(gateway)
                except network.IPMissing, msg:
                    self._handleIPMissing(_("Gateway"))
                    continue
                except network.IPError, msg:
                    self._handleIPError(_("Gateway"), msg)
                    continue

                try:
                    if ns:
                        network.sanityCheckIPString(ns)
                except network.IPError, msg:
                    self._handleIPError(_("Nameserver"), msg)
                    continue

                try:
                    isys.configNetDevice(netdev, gateway)
                except Exception, e:
                    import logging
                    log = logging.getLogger("anaconda")
                    log.error("Error configuring network device: %s" % e)
                    self._handleIPError(_("Error configuring network device: "), e)
                    self.screen.popWindow()
                    return INSTALL_BACK

                if ns:
                    f = open("/etc/resolv.conf", "w")
                    f.write("nameserver %s\n" % ns)
                    f.close()
                    isys.resetResolv()
                    isys.setResolvRetry(1)
                    break

            break

        self.screen.popWindow()
        return INSTALL_OK