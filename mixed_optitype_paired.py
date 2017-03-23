#!/usr/bin/env python

# Imports glob module
import glob

# Imports and initializes optparse module
import optparse
p = optparse.OptionParser()

def optitype_job(run, study, seq):
	# Sets suffixes for read 1 and read 2 files and directory
	read1 = "_1.fastq.gz"
	read2 = "_2.fastq.gz"
	directory = "/mnt/lustre1/CompBio/data/immunotherapy/" + study + "/"
	# Sets file names
	firstread = directory + run + read1
	secondread = directory + run + read2
	# Sets paths to shell, submit, and master scripts for job
	shell_script = "/home/users/wooma/jobs/shell_scripts/optitype/" + run + ".sh"
	submit_script = "/home/users/wooma/jobs/submit_scripts/optitype/" + run + ".submit" 
	job_master = "/home/users/wooma/jobs/shell_scripts/optitype/MASTER_" + study + ".sh"
	# Sets paths to error, log, and outfiles for job
	errorfile = "/home/users/wooma/jobs/error/optitype/" + run + ".error" 
	logfile = "/home/users/wooma/jobs/log/optitype/" + run + ".log"
	outputfile = "/home/users/wooma/jobs/out/optitype/" + run + ".out"
	# Sets paths to optitype resources and to output directory
	optitype_path = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/optitype/"
	config_file = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/optitype/config.ini"
	out_dir = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/"
	# Sets optitype commands
	venv_activate = ". /mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/optitype/venv2/bin/activate"
	optitype = "python " + optitype_path + "OptiTypePipeline.py -i " + firstread + " " + secondread + " --" + seq + " --enumerate 5 --outdir " + out_dir + " --verbose --config " + config_file + " --prefix " + run
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n")
	shellfh.write(venv_activate + "\n")
	shellfh.write(optitype + "\n")
	shellfh.write("deactivate\n")
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

# Adds study and seq type options to command line
p.add_option("-s", action="store", dest="study")

# Parse command line for study
opts, args = p.parse_args()
current_study = opts.study

# Initializes master file to spawn jobs
master_file = "/home/users/wooma/jobs/shell_scripts/optitype/MASTER_" + current_study + ".sh"
fh1 = open(master_file, "w")
fh1.write("#!/bin/bash\n")
fh1.close()

dna_runs_list = "/home/users/wooma/" + current_study + "_WES.txt"
rna_runs_list = "/home/users/wooma/" + current_study + "_RNAseq.txt"

fh1 = open(dna_runs_list, "r")
fh2 = open(rna_runs_list, "r")


for line in fh1:
	line = line.strip("\n")
	optitype_job(line, current_study, "dna")


for line in fh2:
	line = line.strip("\n")
	optitype_job(line, current_study, "rna")

fh1.close()
fh2.close()