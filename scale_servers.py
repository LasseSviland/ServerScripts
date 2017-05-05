#!/usr/bin/python

import math
import argparse
import subprocess

VERBOSE = 0
DEBUG = 0

IP = ""
USER = ""
PASSWORD = ""

RATE_PER_SERVER = 5
MAX_SERVERS = 10
MIN_SERVERS = 1



###################################################################################################
# Argument handeling
parser = argparse.ArgumentParser(prog='scale_servers.py')
parser.add_argument('-v','--verbose',dest="verbose",help="Turn on verbosity",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn on debug information",default=False,action="store_true")
parser.add_argument('-i','--ip',dest="ip",help="IP address of haproxy server",default=IP)
parser.add_argument('-u','--user',dest="user",help="User for haproxy authentication",default=USER)
parser.add_argument('-p','--password',dest="password",help="Password for haproxy authentication",default=PASSWORD)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
IP = arguments.ip
USER = arguments.user
PASSWORD = arguments.password
###################################################################################################

def verbose(text):
    if VERBOSE:
        print "VERBOSE: " + text

def debug(text):
    if DEBUG:
        print "DEBUG: " + text

def get_rate(user, password, ip):
    url = "http://" + user + ":" + password +"@" + ip + ":1936/;csv"
    debug("Using url:" + url)
    output = subprocess.check_output(["curl", "-s", url])
    for line in output.split("\n"):
        if "bookface" in line:
            stats_array = line.split(',')
            total_rate = stats_array[33]
            return float(total_rate)


def get_workers():
    output = subprocess.check_output("source logininfo.sh; openstack server list | grep www | grep ACTIVE | wc -l",executable="/bin/bash",shell=True)
    output = output.rstrip()
    return float(output)

def get_server_with_status(status, server_num):
    command = "source logininfo.sh; openstack server list -f value | grep www | grep " + status + " | sed -n " + str(server_num) + "p | awk '{print $2}'"
    output = subprocess.check_output(command,executable="/bin/bash",shell=True)
    return output.rstrip()

def scale_up(current, goal):
    for i in range(0, (goal - current)):
        verbose("Starting server: " + str(i+1))
        command = "source logininfo.sh; openstack server start " + get_server_with_status("SHUTOFF", i+1)
        debug("Running command: " + command)
        output = subprocess.check_output(command,executable="/bin/bash",shell=True)

def scale_down(current, goal):
    for i in range(0, (current - goal)):
        verbose("Stopping server : " + str(i))
        command = "source logininfo.sh; openstack server stop " + get_server_with_status("ACTIVE", i+1)
        debug("Running command: " + command)
        output = subprocess.check_output(command,executable="/bin/bash",shell=True)

# get current rate
current_rate = get_rate(USER, PASSWORD, IP)
verbose("Current rate: " + str(current_rate))


# get current number of workers
current_workers = get_workers()
verbose("Current workers: " + str(current_workers))

# calculate current needed capacity
needed_capacity = math.ceil(current_rate / RATE_PER_SERVER)
verbose("We need " + str(needed_capacity) + " servers to handle this rate")
if needed_capacity < MIN_SERVERS :
    needed_capacity = MIN_SERVERS
    verbose("Adjusting needed capacity to minimum:" + str(needed_capacity))
elif needed_capacity > MAX_SERVERS :
    needed_capacity = MAX_SERVERS
    verbose("Adjusting needed capacity to maximum:" + str(needed_capacity))

# compare current needed with actual capacity and take action (reduce or increase servers)
if needed_capacity > current_workers :
    verbose("We need to increase the number of servers from " + str(current_workers) + " to " + str(needed_capacity))
    scale_up(int(current_workers), int(needed_capacity))
elif needed_capacity < current_workers :
    verbose("We need to reduce the number of servers from " + str(current_workers) + " to " + str(needed_capacity))
    scale_down(int(current_workers), int(needed_capacity))
else:
    verbose("No action taken")






