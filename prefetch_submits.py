#!/usr/bin/env python

# Defines a function to prefetch from SRA and follow with fastqdump (no gzip)
def prefetch_job(study, run):
	# Sets directories/paths for relevant tools ## PLEASE DOUBLE CHECK THESE ##
	sra_dir = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/sratoolkit.2.8.1-3-centos_linux64/bin/"
	aspera_dir= "/home/users/wooma/.aspera/connect/bin/"
	aspera_ssh= "/home/users/wooma/.aspera/connect/etc/asperaweb_id_dsa.openssh"
	ncbi_dir = "/home/users/wooma/ncbi/public/"
	# Sets destination directory
	destination = "/mnt/lustre1/CompBio/data/immunotherapy/" + study + "/"
	# Sets paths to shell, submit, and master scripts for job ## PLEASE DOUBLE CHECK THESE ##
	shell_script = "/home/users/wooma/jobs/shell_scripts/downloads/" + run + ".sh"
	submit_script = "/home/users/wooma/jobs/submit_scripts/downloads/" + run + ".submit" 
	job_master = "/home/users/wooma/jobs/shell_scripts/downloads/MASTER.sh"
	# Sets paths to error, log, and outfiles for job  ## PLEASE DOUBLE CHECK THESE ##
	errorfile = "/home/users/wooma/jobs/error/downloads/" + run + ".error" 
	logfile = "/home/users/wooma/jobs/log/downloads/" + run + ".log"
	outputfile = "/home/users/wooma/jobs/out/downloads/" + run + ".out"
	# Sets commands to execute ## PLEASE DOUBLE CHECK THESE ##
	prefetch = sra_dir + 'prefetch -t ascp -a "' + aspera_dir + 'ascp|' + aspera_ssh + '" -c ' + run + ' --verbose --verbose --verbose'
	move_file = "mv " + ncbi_dir + "sra/" + run + ".sra " + destination
	fastq_dump = sra_dir + 'fastq-dump -I --split-files --gzip -O ' + destination + ' ' + destination + run + '.sra'
	sra_stat = sra_dir + "sra-stat --quick --xml " + destination + run + ".sra > /mnt/lustre1/CompBio/data/immunotherapy/SRA_stats/" + run + "_stats.xml"
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n")
	shellfh.write("cd " + ncbi_dir + "\n")
	shellfh.write(prefetch + "\n")
	shellfh.write(move_file + "\n")
	shellfh.write(fastq_dump + "\n")
	shellfh.write(sra_stat + "\n")
	shellfh.close()
	# Writes the submit file
	submitfh = open(submit_script, "w")
	submitfh.write("universe = vanilla\n")
	submitfh.write("getenv= true\n")
	submitfh.write("executable = " + shell_script + "\n")
	submitfh.write("error = " + errorfile + "\n")
	submitfh.write("log = " + logfile + "\n")
	submitfh.write("output = " + outputfile + "\n")
	submitfh.write("queue")
	submitfh.close()
	# Appends commands to make shell script executable and submit the submit file to the master shell script
	masterfh = open(job_master, "a")
	masterfh.write("chmod u+x " + shell_script + "\n")
	masterfh.write("condor_submit " + submit_script + "\n")
	masterfh.close()

# Opens files with lists of missing runs for reading ## MAY NEED TO EDIT PATHS IF YOU CAN'T ACCESS THESE ##
#fh1 = open("/home/users/wooma/PRJNA307199_runs.txt", "r")
#fh2 = open("/home/users/wooma/PRJNA324705_runs.txt", "r")
fh2 = open("/home/users/wooma/PRJNA343789_runs.txt", "r")

# Initializes master file to spawn jobs
fh3 = open("/home/users/wooma/jobs/shell_scripts/downloads/MASTER.sh", "w") ## PLEASE DOUBLE CHECK ##
fh3.write("#!/bin/bash\n")
fh3.close()

# Loops through missing files in the PRJNA307199 study to write files for a prefetch job
#for line in fh1:
#	line = line.strip('\n')
#	prefetch_job("PRJNA307199", line)

# Loops through missing files in the PRJNA343789 study to write files for a prefetch job	
for line in fh2:
	line = line.strip('\n')
	prefetch_job("PRJNA343789", line)