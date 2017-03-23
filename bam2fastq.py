#!/usr/bin/env python

# Imports glob module
import glob

def bam2fastq_job(bamfile):
	# Obtains file prefix
	prefix = bamfile.strip("Ex.bam").strip("_").split("/")[-1]		
	# Sets shell script, submit file, and master script for the job
	shell_script = "/home/users/wooma/jobs/shell_scripts/bam2fastq/" + prefix + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/bam2fastq/" + prefix + ".submit"
	job_master = "/home/users/wooma/jobs/shell_scripts/bam2fastq/MASTER_Hopkins.sh"
	# Sets error, out, and log files for the job
	errorfile = "/home/users/wooma/jobs/error/bam2fastq/" + prefix + ".error"
	outfile = "/home/users/wooma/jobs/out/bam2fastq/" + prefix + ".out"
	logfile = "/home/users/wooma/jobs/log/bam2fastq/" + prefix + ".log"
	# Sets path to picard, output dir, outfiles, and commands
	picard_clean = "java -jar /opt/installed/picard/picard-tools-1.110/CleanSam.jar"
	picard_sam2fastq = "java -jar /opt/installed/picard/picard-tools-1.110/SamToFastq.jar"
	output_dir = "/mnt/lustre1/CompBio/data/immunotherapy/Hopkins/"
	cleaned_file = output_dir + prefix + "_cleaned.bam"
	outfile1 = output_dir + prefix + "_1.fastq"
	outfile2 = output_dir + prefix + "_2.fastq"
	cleansam = picard_clean + " INPUT=" + bamfile + " OUTPUT=" + cleaned_file
	bam2fastq = picard_sam2fastq + " INPUT=" + cleaned_file + " INCLUDE_NON_PF_READS=true FASTQ=" + outfile1 + " SECOND_END_FASTQ=" + outfile2
	gzip1 = "gzip " + outfile1
	gzip2 = "gzip " + outfile2
	# Writes the shell script for the job
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash\n")
	fh1.write(cleansam + "\n")
	fh1.write(bam2fastq + "\n")
	fh1.write(gzip1 + "\n")
	fh1.write(gzip2 + "\n")
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

# Initiates master file to spawn jobs
master_file = "/home/users/wooma/jobs/shell_scripts/bam2fastq/MASTER_Hopkins.sh"
masterfh = open(master_file, "w")
masterfh.write("#!/bin/bash\n")
masterfh.close()

# Creates a string for the directory to search
directory = "/mnt/lustre1/CompBio/data/immunotherapy/Hopkins/*.bam"

# Obtains list of read 1 files in the directory
directory_files = glob.glob(directory)

# Loops through the files and writes bam2fastq job scripts for each file
for file in directory_files:
	bam2fastq_job(file)
