#!/usr/bin/env python

# Imports glob and os modules
import glob
import os

# Defines a function to write a shell script and submit file
# The job will perform fastq dump for an sra file, then check gzip compression of the resulting fastq files
def write_gzipcheck_submit(file):
	# Establishes study and file prefix names
	prefix = file.strip(".sra").split("/")[-1]
	study = file.strip(".sra").split("/")[-2]
	# Sets the paths to shell script and submit file for the 
	shell_script = "/home/users/wooma/jobs/shell_scripts/fastq_checks/" + prefix + ".sh"
	submit_file = "/home/users/wooma/jobs/submit_scripts/fastq_checks/" + prefix + ".submit"
	# Sets path to the master shell script that will execute all jobs
	job_master = "/home/users/wooma/jobs/shell_scripts/fastq_checks/MASTER.sh"
	# Sets paths to the error and output files for the job
	errorfile = "/home/users/wooma/jobs/error/fastq_checks/" + prefix + ".error"
	outputfile = "/home/users/wooma/gzip_check_output/" + prefix + ".out"
	# Sets the path for the SRA toolkit
	SRA_toolkit_path = "/home/users/wooma/sratoolkit.2.8.1-2-centos_linux64/bin/"
	# Sets commands for fastq_dump and gunzip
	fastq_dump = SRA_toolkit_path + "fastq-dump --split-files --gzip -O /mnt/lustre1/CompBio/data/immunotherapy/" + study + " /mnt/lustre1/CompBio/data/immunotherapy/" + study + "/" + prefix + ".sra"
	#fastq_dump = "/opt/installed/fastq-dump --split-files --gzip -O /mnt/lustre1/CompBio/data/immunotherapy/" + study + " /mnt/lustre1/CompBio/data/immunotherapy/" + study + "/" + prefix + ".sra"
	gunzip = "gunzip -t /mnt/lustre1/CompBio/data/immunotherapy/" + study + "/" + prefix + "*fastq.gz"
	# Writes the shell script
	fh1 = open(shell_script, "w")
	fh1.write("#!/bin/bash" + "\n")
	fh1.write("/home/users/wooma/sratoolkit.2.8.1-2-centos_linux64/bin/vdb-config --import /mnt/lustre1/CompBio/projs/RThompson/immunotherapy/prj_12172.ngc" + "\n")
	fh1.write(fastq_dump + "\n")
	fh1.write(gunzip + "\n")
	fh1.close()
	# Writes the submit file
	fh2 = open(submit_file, "w")
	fh2.write("universe = vanilla" + "\n")
	fh2.write("executable = " + shell_script + "\n")
	fh2.write("error = " + errorfile + "\n")
	fh2.write("output = " + outputfile + "\n")
	fh2.write("queue")
	fh2.close()
    # Appends commands to make shell script executable and submit the submit file to the master shell script
	fh3 = open(job_master, "a")
	fh3.write("chmod u+x " + shell_script + "\n")
	fh3.write("condor_submit " + submit_file + "\n")
	fh3.close()

# Creates a list of all subdirectory and file names in the immunotherapy directory
directory_list = os.listdir("/mnt/lustre1/CompBio/data/immunotherapy/")

# Removes any non-"PRJ" subdirectories/files
for item in directory_list:
	if "PRJ" not in item:
		directory_list.remove(item)

# Initiates master file to spawn jobs
masterfh = open("/home/users/wooma/jobs/shell_scripts/fastq_checks/MASTER.sh", "w")
masterfh.write("#!/bin/bash\n")
masterfh.close()

# Loops through each directory and obtains its path
# For each file in the directory, a submit file is written
#for directory in directory_list:
#	path = "/mnt/lustre1/CompBio/data/immunotherapy/" + directory + "/*.sra"
#	files = glob.glob(path)
#	#for file in files:
#	for file in files[0:3]:
#		write_gzipcheck_submit(file)

study = directory_list[2]
path = "/mnt/lustre1/CompBio/data/immunotherapy/" + study + "/*.sra"
files = glob.glob(path)
for file in files[0:3]:
	write_gzipcheck_submit(file)
