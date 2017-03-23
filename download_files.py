#!/usr/bin/env python

# Create an empty list to hold runs for the study
run_list = []

# Loops through all files for the study to save as runs in the run list
for i in range(37, 84): ##### 14, 45 ; 37, 84
	run_num = str(i)
	run = "SRR30838" + run_num ##### SRR42897 ; SRR30838
	run_list.append(run)

# Opens file containing list of runs for which fastq file download is not available	
missing_runs = open("/home/users/wooma/PRJNA307199_runs.txt", "r") ##### PRJNA343789 ; PRJNA307199

# Removes runs for which fastq file download is not available
for line in missing_runs:
	line = line.strip("\n")
	run_list.remove(line)

# Defines a function to write scripts for submitting jobs to download available files
def download_fastqs(run):
	# Sets destination directory
	destination = "/mnt/lustre1/CompBio/data/immunotherapy/PRJNA307199/" ##### PRJNA343789 ; PRJNA307199
	# Sets wget links for read1 and read 2 files
	r1link = "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR308/00" + run[-1] + "/" + run + "/" + run + "_1.fastq.gz" ##### SRR428 ; SRR308
	r2link = "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR308/00" + run[-1] + "/" + run + "/" + run + "_2.fastq.gz" ##### SRR428 ; SRR308
	# Sets paths to shell, submit, error, and master scripts for job
	shell_script = "/home/users/wooma/jobs/shell_scripts/downloads/" + run + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/downloads/" + run + ".submit" 
	job_master = "/home/users/wooma/jobs/shell_scripts/downloads/MASTER2.sh" ##### ; 2
	errorfile = "/home/users/wooma/jobs/error/downloads/" + run + ".error"
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n")
	shellfh.write("cd " + destination + "\n")
	shellfh.write("wget " + r1link + "\n")
	shellfh.write("wget " + r2link + "\n")
	shellfh.close()
	# Writes the submit file
	submitfh = open(submit_file, "w")
	submitfh.write("universe = vanilla\n")
	submitfh.write("getenv= true\n")
	submitfh.write("executable = " + shell_script + "\n")
	submitfh.write("error = " + errorfile + "\n")
	submitfh.write("queue")
	submitfh.close()
	# Appends commands to make shell script executable and submit the submit file to the master shell script
	masterfh = open(job_master, "a")
	masterfh.write("chmod u+x " + shell_script + "\n")
	masterfh.write("condor_submit " + submit_file + "\n")
	masterfh.close()
	
# Initializes master file to spawn jobs
fh3 = open("/home/users/wooma/jobs/shell_scripts/downloads/MASTER2.sh", "w") ##### ; 2
fh3.write("#!/bin/bash\n")
fh3.close()

# Writes job files for each run
for run in run_list:
	download_fastqs(run)
