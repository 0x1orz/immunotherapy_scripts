#!/usr/bin/env python

# Imports glob module
import glob

# Imports and initializes optparse module
import optparse
p = optparse.OptionParser()

# Defines a function that writes submit scripts for running fastqc and bwa for paired end files
def write_bwa_submit(dictionary, key, study):
	# Sets first and second read files and file prefix
	firstread = dictionary[key][0]
	secondread = dictionary[key][1]
	prefix = key
	# Sets sed commands for each file for use in bwa to fix header lines
	read1sed = "<(gzip -cd " + firstread + " | sed -E 's~^(@.+[.][0-9]+)[.][1] .+( length=[0-9]+)~\\1/1\\2~')"
	read2sed = "<(gzip -cd " + secondread + " | sed -E 's~^(@.+[.][0-9]+)[.][2] .+( length=[0-9]+)~\\1/2\\2~')"
	# Sets shell script, submit file, and master script for the job
	shell_script = "/home/users/wooma/jobs/shell_scripts/bwa/" + prefix + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/bwa_submits/" + prefix + ".submit"
	job_master = "/home/users/wooma/jobs/shell_scripts/bwa/MASTER_" + study + ".sh"
	# Sets error and log files for the job
	errorfile = "/home/users/wooma/jobs/error/bwa_errors/" + prefix + ".error"
	logfile = "/home/users/wooma/jobs/log/bwa_logs/" + prefix + ".log"
	outfile = "/home/users/wooma/jobs/out/bwa_out/" + prefix + ".out"
	# Sets the fastqc command for each file in the read pair
	fastqc1 = "/opt/installed/fastqc -o /mnt/lustre1/CompBio/data/immunotherapy/FastQC/ " + firstread
	fastqc2 = "/opt/installed/fastqc -o /mnt/lustre1/CompBio/data/immunotherapy/FastQC/ " + secondread
	# Sets the output bam file from bwa
	output = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + prefix + ".bam"
	# Sets the bwa command for each file in the read pair
	bwa = "/opt/installed/bwa mem -T 0 /mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/Homo_sapiens_assembly38.fasta " + read1sed + " " + read2sed + " > " + output
	# Writes the shell script for the job
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash" + "\n")
	#fh1.write(fastqc1 + "\n")
	#fh1.write(fastqc2 + "\n")
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
masterfh.close()

# Creates a string for the directory to search
directory = "/mnt/lustre1/CompBio/data/immunotherapy/" + current_study + "/*1.fastq.gz"

# Obtains list of read 1 files in the directory
directory_files = glob.glob(directory)

# Creates a dictionary to hold read pairs
# Key: File prefix, entry: list of paths to read 1 and read 2
read_pairs = {}

# Suffixes for read 1 and read 2 files
read1 = "_1.fastq.gz"
read2 = "_2.fastq.gz"

# Loops through the list of read 1 files
# Strips the read 1 suffix off the each file
# Obtains the file prefix
# Writes the prefix key and read 1/read 2 entry list to the read_pairs dictionary
for file in directory_files:
	file = file.strip("1.fastq.gz").strip("_")
	prefix = file.split("/")[-1]
	first_file = file + read1
	second_file = file + read2
	read_pairs[prefix] = [first_file, second_file]

# Writes a condor submit file for each read pair	
for pair in read_pairs:
	write_bwa_submit(read_pairs, pair, current_study)
