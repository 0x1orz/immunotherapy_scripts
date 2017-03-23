#!/usr/bin/env python

# Imports glob module
import glob

# Defines a function to write files for submitting a cram to fastq conversion job for a file
def write_cramtofastq_jobs(file):
	# Establishes file prefix name
	prefix = file.strip(".cram").split("/")[-1]
	# Sets the paths to shell script and submit file for the job
	shell_script = "/home/users/wooma/jobs/shell_scripts/cram2fq/" + prefix + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/cram2fq/" + prefix + ".submit"
	# Sets path to the master shell script that will execute all jobs
	job_master = "/home/users/wooma/jobs/shell_scripts/cram2fq/MASTER.sh"
	# Sets paths to the error and output files for the job
	errorfile = "/home/users/wooma/jobs/error/cram2fq/" + prefix + ".error"
	# Sets output directory for the fastq files and intermediate sam files
	fastqdir = "/home/users/wooma/EGAD00001001985_fastqs/"
	# Designates output bam file and read1, read2, and unpaired fastq files
	bamout = fastqdir + prefix + ".bam"
	fastq1 = fastqdir + prefix + "_1.fastq"
	fastq2 = fastqdir + prefix + "_2.fastq"
	unpaired = fastqdir + prefix + "_unpaired.fastq"
	# Writes samtools view command to convert the cram file to a bam file for picard SamtoFastq
	# Includes option to output in bam format (-b), to include header in output (-h), and to specify outfile (-o)
	samtools_view = "/opt/installed/samtools view -b -h -o " + bamout + " " + file
	# Writes the first part of the picard SamToFastq command
	picards2f = "java -jar /opt/installed/picard/picard-tools-1.110/picard-1.110.jar SamToFastq "
	# Writes picard SamToFastq command
	# Includes outputs for read1, read2, and unpaired reads, and includes files that don't pass quality filter
	sam2fq = picards2f + "I=" + bamout + " FASTQ=" + fastq1 + " SECOND_END_FASTQ=" + fastq2 + " UNPAIRED_FASTQ=" + unpaired + " INCLUDE_NON_PF_READS=true"
	# Writes the shell script
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash" + "\n")
	fh1.write(samtools_view + "\n")
	fh1.write(sam2fq + "\n")
	fh1.close()
	# Writes the submit file
	fh2 = open(submit_file, "w")
	fh2.write("universe = vanilla" + "\n")
	fh2.write("executable = " + shell_script + "\n")
	fh2.write("error = " + errorfile + "\n")
	fh2.write("queue")
	fh2.close()
	# Appends commands to make shell script executable and submit the submit file to the master shell script
	fh3 = open(job_master, "a")
	fh3.write("chmod u+x " + shell_script + "\n")
	fh3.write("condor_submit " + submit_file + "\n")
	fh3.close()
	

# Initiates master shell script to spawn jobs
masterfh = open("/home/users/wooma/jobs/shell_scripts/cram2fq/MASTER.sh", "w")
masterfh.write("#!/bin/bash\n")
masterfh.close()

# Loops through all cram files in the directory and writes scripts for cram to fastq jobs for each
directory = "/mnt/lustre1/CompBio/data/immunotherapy/EGAD00001001985/*.cram"
files = glob.glob(directory)
#for file in files:
for file in files[0:3]:
	write_cramtofastq_jobs(file)
