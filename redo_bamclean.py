#!/usr/bin/env python

import subprocess

runfile = "/home/users/wooma/redo_runs.txt"
fh = open(runfile, "r")

for line in runfile:
    run = line.strip("\n")
    #command = "condor_submit"
    submit_file = "/home/users/wooma/jobs/submit_scripts/bam_cleaning/" + run + ".submit"
    subprocess.call("condor_submit " + submit_file)
