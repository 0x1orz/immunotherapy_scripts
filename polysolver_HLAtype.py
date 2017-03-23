#!/usr/bin/env python

# Imports glob module
import glob

def polysolver_HLAtype_job(bam):
	# Obtains the run name from the bam file path
	run = bam.strip(".bam").split("/")[-1]
	# Sets paths to shell, submit, and master scripts for job
	shell_script = "/home/users/wooma/jobs/shell_scripts/polysolver/" + run + ".sh"
	submit_script = "/home/users/wooma/jobs/submit_scripts/polysolver/" + run + ".submit" 
	job_master = "/home/users/wooma/jobs/shell_scripts/polysolver/MASTER.sh"
	# Sets paths to error, log, and outfiles for job
	errorfile = "/home/users/wooma/jobs/error/polysolver/" + run + ".error" 
	logfile = "/home/users/wooma/jobs/log/polysolver/" + run + ".log"
	outputfile = "/home/users/wooma/jobs/out/polysolver/" + run + ".out"
	# Sets paths to polysolver and to output directory
	polysolver_path = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/new_polysolver/"
	workspace_dir = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/polysolver_workspace/"
	out_dir = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/"
	# Sets polysolver commands
	configure = "source " + polysolver_path + "scripts/config.bash"
	hla_type = polysolver_path + "scripts/shell_call_hla_type " + bam + " Unknown 1 hg38 STDFQ 1 " + workspace_dir
	move_final = "mv " + workspace_dir + "winners.hla.txt " + out_dir + run + ".winners.hla.txt"
	clear_dir = "rm " + workspace_dir + "*"
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n")
	shellfh.write(configure + "\n")
	shellfh.write(hla_type + "\n")
	shellfh.write(move_final + "\n")
	shellfh.write(clear_dir + "\n")
	shellfh.close()
	# Writes the submit file
	submitfh = open(submit_script, "w")
	submitfh.write("universe = vanilla\n")
	submitfh.write("getenv= true\n")
	submitfh.write("request_memory=15 GB\n")
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


# Initializes master file to spawn jobs
fh1 = open("/home/users/wooma/jobs/shell_scripts/polysolver/MASTER.sh", "w")
fh1.write("#!/bin/bash\n")
fh1.close()

# Creates a string for the directory to search
directory = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/old/*.bam"

# Obtains list of read 1 files in the directory
directory_files = glob.glob(directory)

for file in directory_files:
	polysolver_HLAtype_job(file)