#!/usr/bin/env python

# Imports glob module
import glob

# Imports and initializes optparse module
import optparse
p = optparse.OptionParser()

# Defines a function that writes submit scripts for running fastqc and bwa
def write_bwa_submit(file):
	# Sets prefix and sed command for the file
	prefix = file.strip(".fastq.gz").split("/")[-1]
	study = file.strip(".fastq.gz").split("/")[-2]
	# Sets shells script, submit file, error file, and log file for the job
	shell_script = "/home/users/wooma/jobs/shell_scripts/bwa/" + prefix + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/bwa_submits/" + prefix + ".submit"
	errorfile = "/home/users/wooma/jobs/error/bwa_errors/" + prefix + ".error"
	logfile = "/home/users/wooma/jobs/log/bwa_logs/" + prefix + ".log"
	outfile = "/home/users/wooma/jobs/out/bwa_out/" + prefix + ".out"
	# Sets master shell script for all jobs in study
	job_master = "/home/users/wooma/jobs/shell_scripts/bwa/MASTER_" + study + ".sh"
	# Sets bam output file
	output = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + prefix + ".bam"
	# Sets fastqc and bwa commands
	fastqc = "/opt/installed/fastqc -q -o /mnt/lustre1/CompBio/data/immunotherapy/FastQC/ " + file
	bwa = "/opt/installed/bwa mem -T 0 /mnt/lustre1/CompBio/genomic_resources/genomes/hg38/Homo_sapiens.GRCh38.dna.primary_assembly.fa " + file " > " + output
	# Writes the shell script for the job
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash" + "\n")
	fh1.write(fastqc + "\n")
	fh1.write(bwa + "\n")
	fh1.close()
	# Writes the submit file for the job
	fh2 = open(submit_file, "w")
	fh2.write("universe = vanilla" + "\n")
	fh2.write("executable = " + shell_script + "\n")
	fh2.write("log = " + logfile + "\n")
	fh2.write("error = " + errorfile + "\n")
	fh2.write("output = " + outfile + "\n")
	fh2.write("queue")
	fh2.close()
	# Appends commands to the master script for the all the jobs in the study
	fh3 = open(job_master, "a")
	fh3.write("chmod u+x " + shell_script + "\n")
	fh3.write("condor_submit " + submit_file + "\n")
	fh3.close()
	
# Adds study option to command line
p.add_option("-s", action="store", dest="study")

# Parse command line for study
opts, args = p.parse_args()
current_study = opts.study

# Initiates master file to spawn jobs
master_file = "/home/users/wooma/jobs/shell_scripts/bwa/MASTER_" + current_study + ".sh"
masterfh = open(master_file, "w")
masterfh.write("#!/bin/bash\n")

# Creates a string for the directory to search
directory = "/mnt/lustre1/CompBio/data/immunotherapy/" + current_study + "/*.fastq.gz"

# Obtains list of files in the directory
directory_files = glob.glob(directory)

# Loops through the list of files and write bwa submit scripts
for file in directory_files:
	write_bwa_submit(file)
