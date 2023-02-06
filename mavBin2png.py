#!/usr/bin/env python3
"""
Heavily based on ArduPilot tools code.

"""

import glob
import os
import subprocess
import timeit

from datetime import datetime
from pymavlink import mavutil
from pymavlink.generator import mavtemplate

def cmd_as_shell(cmd):
    return (" ".join(['"%s"' % x for x in cmd]))


def run_cmd(cmd, directory=".", show=True, output=False, checkfail=True):
    """Run a shell command."""
    shell = False
    if not isinstance(cmd, list):
        cmd = [cmd]
        shell = True
    if show:
        print("Running: (%s) in (%s)" % (cmd_as_shell(cmd), directory,))
    if output:
        return subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, cwd=directory).communicate()[0]
    elif checkfail:
        return subprocess.check_call(cmd, shell=shell, cwd=directory)
    else:
        return subprocess.call(cmd, shell=shell, cwd=directory)

def convert_bin_files():
    """Convert BIN logfiles to PNG."""
    mavlog = glob.glob("*.bin")
    passed = True
    # try:
    #     run_cmd('rm %s.png' % (m))
    # except subprocess.CalledProcessError:
    #     pass

    for m in mavlog:
        # get the logID without path and extension
        current_log = m[m.rfind('/') + 1:-5]

        #print('m -> %s' % (m))
        #print('current_log -> %s' % (current_log))

        try:
            run_cmd("mavflightview.py --imagefile=%s.png %s" % (m, m))

        except subprocess.CalledProcessError:
            passed = False

    return passed


def do_log(text):
    try:
        file_object = open('_mavBin2png.py.log', 'a')
        file_object.write(text)
        file_object.write('\n')
        file_object.close()
    except Exception as e:                                
        print("[_mavBin2png.py] Unable to log: ", e)
        pass


starttime = timeit.default_timer()
print("[mavBin2png.py] Starting:", starttime)
#do_log("[mavBin2png.py] Starting: {now}".format(now=(datetime.now())))

run_result = convert_bin_files()

print("[mavBin2png.py] Passed = {passed} | Time = {time} seconds | now = {now}".format(passed=run_result, time=(timeit.default_timer() - starttime), now=(datetime.now())))
#do_log("[mavBin2png.py] Passed = {passed} | Time = {time} seconds | now = {now}".format(passed=run_result, time=(timeit.default_timer() - starttime), now=(datetime.now())))
