#!/usr/bin/env python
'''
casadiplanner Module
Peter Barker, September 2016

This module simply serves as a starting point for your own MAVProxy module.

1. copy this module sidewise (e.g. "cp mavproxy_casadiplanner.py mavproxy_coolfeature.py"
2. replace all instances of "casadiplanner" with whatever your module should be called
(e.g. "coolfeature")

3. trim (or comment) out any functionality you do not need
'''

import os
import os.path
import sys
from pymavlink import mavutil
import errno
import time

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings

import casadiplanner_backend

class casadiplanner(mp_module.MPModule):

    res = 0.0

    def __init__(self, mpstate):
        """Initialise module"""
        super(casadiplanner, self).__init__(mpstate, "casadiplanner", "")
        self.status_callcount = 0
        self.boredom_interval = 10 # seconds
        self.last_bored = time.time()

        self.packets_mytarget = 0
        self.packets_othertarget = 0

        self.casadiplanner_settings = mp_settings.MPSettings(
            [ ('verbose', bool, False),
          ])

        self.add_command('casadiplan', self.cmd_casadiplan, "example module", ['status','set (LOGSETTING)'])

    def usage(self):
        '''show help on command line options'''
        return "Usage: casadiplanner <status|set>"

    def status(self):
        '''returns information about module'''
        self.status_callcount += 1
        self.last_bored = time.time() # status entertains us
        return("status called %(status_callcount)d times.  My target positions=%(packets_mytarget)u  Other target positions=%(packets_mytarget)u" %
               {"status_callcount": self.status_callcount,
                "packets_mytarget": self.packets_mytarget,
                "packets_othertarget": self.packets_othertarget,
               })

    def cmd_casadiplan(self, arg2):
       #print(arg2.toString())
       res=casadiplanner_backend.plan()
       print("Planning result %f" % res)


    def boredom_message(self):
        if self.casadiplanner_settings.verbose:
            return ("I'm very bored")
        return ("I'm very bored")

    def idle_task(self):
        '''called rapidly by mavproxy'''
        now = time.time()
        if now-self.last_bored > self.boredom_interval:
            self.last_bored = now
            message = self.boredom_message()
            self.say("%s: %s" % (self.name,message))
            # See if whatever we're connected to would like to play:
            self.master.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,
                                            message)

    def mavlink_packet(self, m):
        '''handle mavlink packets'''
        if m.get_type() == 'GLOBAL_POSITION_INT':
            if self.settings.target_system == 0 or self.settings.target_system == m.get_srcSystem():
                self.packets_mytarget += 1
            else:
                self.packets_othertarget += 1

def init(mpstate):
    '''initialise module'''
    return casadiplanner(mpstate)
