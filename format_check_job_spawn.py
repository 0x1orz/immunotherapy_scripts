#!/usr/bin/env python

# Imports glob module
import glob

# Defines function to spawn jobs to check fastq formatting
def check_formats(label):
	# Isolates just the run label from the entire path label
	run = label.split("/")[-1]
	# Establishes paths to files for the job
	shell_script = "/home/users/wooma/jobs/shell_scripts/fastq_checks/" + run + ".sh" # EDIT
	submit_file = "/home/users/wooma/jobs/submit_scripts/fastq_checks/" + run + ".submit" # EDIT
	job_master = "/home/users/wooma/jobs/shell_scripts/fastq_checks/MASTER.sh" # EDIT
	initial_dir = "/home/users/wooma/jobs/tempfiles/" # EDIT
	error_file = "/home/users/wooma/jobs/error/fastq_checks/" + run + ".error" # EDIT
	log_file = "/home/users/wooma/jobs/log/fastq_checks/" + run + ".log" # EDIT
	out_file = "/home/users/wooma/jobs/out/fastq_checks/" + run + ".out" # EDIT
	# Sets the fastq.gz files to be acted on
	file1 = label + "_1.fastq.gz"
	file2 = label + "_2.fastq.gz"
	# Sets the gunzip commands
	gunzip1 = "gunzip -t " + file1
	gunzip2 = "gunzip -t " + file2
	# Sets the files where the line with total spots will be written for each fastq.gz file
	spots_file1 = initial_dir + run + "_1.txt"
	spots_file2 = initial_dir + run + "_2.txt"
	# Sets commands to obtain line with total spots
	spots1 = "zcat " + file1 + " | tail -4 | head -1 > " + spots_file1
	spots2 = "zcat " + file2 + " | tail -4 | head -1 > " + spots_file2
	# Sets the command to execute the python script that checks for gzip errors and non-matching spots
	python = "python /home/users/wooma/spot_checker.py --err " + error_file + " --f1 " + spots_file1 + " --f2 " + spots_file2 + " --lab " + label
	# Writes the shell script
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash\n")
	fh1.write(gunzip1 + "\n")
	fh1.write(gunzip2 + "\n")
	fh1.write(spots1 + "\n")
	fh1.write(spots2 + "\n")
	fh1.write(python + "\n")
	fh1.write("rm " + spots_file1 + "\n")
	fh1.write("rm " + spots_file2 + "\n")
	fh1.close()
    # Writes the submit file
	fh2 = open(submit_file, "w")
	fh2.write("universe = vanilla\n")
	fh2.write("initialdir = " + initial_dir + "\n")
	fh2.write("executable = " + shell_script + "\n")
	fh2.write("error = " + error_file + "\n")
	fh2.write("log = " + log_file + "\n")
	fh2.write("output = " + out_file + "\n")
	fh2.write("queue")
	fh2.close()
    # Appends commands to make shell script executable and submit the submit file to the master shell script
	fh3 = open(job_master, "a")
	fh3.write("chmod u+x " + shell_script + "\n")
	fh3.write("condor_submit " + submit_file + "\n")
	fh3.close()

# Initiates master file to spawn jobs
masterfh = open("/home/users/wooma/jobs/shell_scripts/fastq_checks/MASTER.sh", "w") # EDIT
masterfh.write("#!/bin/bash\n")
masterfh.close()

# Initiates files to hold violators of gunzip -t test and spot match test
gzipfh = open("/home/users/wooma/jobs/out/fastq_checks/gzip_violators.txt", "w") # EDIT
gzipfh.close()
spotsfh = open("/home/users/wooma/jobs/out/fastq_checks/spot_match_violators.txt", "w") # EDIT
spotsfh.close()

# Generates list read 1 fastq.gz files in the directory
directory = "/mnt/lustre1/CompBio/data/immunotherapy/PRJNA307199/*_1.fastq.gz" # EDIT
file_list = glob.glob(directory)

# For each file, writes scripts for job spawning to check fastq formatting
for file in file_list:
	prefix = file.rstrip("1.fastq.gz").rstrip("_")
	check_formats(prefix)
	