#!/usr/bin/python

import os
import shutil
import argparse

VERBOSE = 0
DEBUG = 0

ITERATIONS = 7
BACKUP_FOLDER = "/backup/"
CONFIG = "/etc/backup.conf"

SCP_USER = "root@"

###################################################################################################
# Argument handeling
parser = argparse.ArgumentParser(prog='pull_backup_dynamisk.py')
parser.add_argument('-v','--verbose',dest="verbose",help="Turn on verbosity",default=False,action="store_true")
parser.add_argument('-d','--debug',dest="debug",help="Turn on debug information",default=False,action="store_true")
parser.add_argument('-c','--config',dest="config",help="Config file to use",metavar="FILE",default=CONFIG)
parser.add_argument('-i','--iterations',dest="iterations",help="How many backup iterations to do",type=int,metavar="N",default=ITERATIONS)
parser.add_argument('-b','--backup-directory',dest="backup_folder",help="Hhere to keep the backup files",metavar="FOLDER",default=BACKUP_FOLDER)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
ITERATIONS = arguments.iterations
CONFIG = str(arguments.config)
BACKUP_FOLDER = str(arguments.backup_folder)
###################################################################################################

def verbose(text):
    if VERBOSE:
        print "VERBOSE: " + text

def debug(text):
    if DEBUG:
        print "DEBUG: " + text

verbose("Opening config file " + CONFIG)
servers = 
ssh ubuntu@$1 sudo cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/authorized_keys
with open(CONFIG) as config:
    for line in config:
        verbose("Read line: " + line)
        configlist = line.split(":")
        paths = "/etc"
        pathlist = paths.split(",")
        verbose("Host: " + configlist[0])
        host = configlist[0]
        if os.system("ssh -oStrictHostKeyChecking=no root@10.1.0.60 uptime") != 0
            continue

        # 0. sjekk at mappen finnes
        host_backup_path = BACKUP_FOLDER + host
        if not os.path.isdir(host_backup_path):
            verbose("Creating nase sync folder " + host_backup_path)
            os.makedirs(host_backup_path)

        # 1. slett den eldste mappen, bare hvis den finnes
        if os.path.isdir(host_backup_path + "." + str(ITERATIONS)):
            verbose("Deleting oldest version of backup directory")
            shutil.rmtree(host_backup_path + "." + str(ITERATIONS))

        # 2. roter mappene fra hoy til lav
        for i in range((ITERATIONS -1 ), 0, -1):
            debug("Checking if " + str(i) + "th/st folder exists")
            if os.path.isdir(host_backup_path + "." + str(i)):
                verbose("Moving older version of backup directory")
                shutil.move(host_backup_path + "." + str(i), host_backup_path + "." + str(i+1))

        # 3. cp -al host til host.1
        verbose("Copying main folder with hard links")
        os.system("cp -al " + host_backup_path + "/* " + host_backup_path + ".1")
        # cp -al /backups/db1 /backups/db1.1
        
        # 4. sync host fra original host med rsync
        verbose("Synchronizing folders")
        for folder in pathlist:
            folder = folder.rstrip()
            verbose("-> " + folder)
            if not os.path.isdir(host_backup_path + folder):
                os.makedirs(host_backup_path + folder)

            verbose_rsync = ""
            if VERBOSE:
                verbose_rsync = "v"

            os.system("rsync -a" + verbose_rsync + " --delete " + SCP_USER + host + ":"  + folder + " " + host_backup_path + " > /dev/null")
