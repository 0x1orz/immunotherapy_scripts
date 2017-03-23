#!/usr/bin/env python

import glob
import subprocess
import os

directory = "/home/users/wooma/jobs/submit_scripts/polysolver/"
submit_files = os.listdir(directory)


for file in submit_files:
	prefix = file.strip(".submit")
	submit_file = "/home/users/wooma/jobs/submit_scripts/polysolver/" + file
	logfile = "/home/users/wooma/jobs/log/polysolver/" + prefix + ".log"
	subprocess.call(['condor_submit', submit_file], shell=False)
	subprocess.call(['condor_wait', logfile], shell=False)