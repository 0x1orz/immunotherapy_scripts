#!/usr/bin/env python

# Imports glob module
import glob

# Defines a function to write a shell script and submit file
# The job will perform fastq dump for an sra file, then check gzip compression of the resulting fastq files
def write_fastqdump_submit(file):
        # Establishes study and file prefix names
        prefix = file.strip(".sra").split("/")[-1]
        # Sets the paths to shell script and submit file for the
        shell_script = "/home/users/wooma/jobs/shell_scripts/sra_debug/" + prefix + ".sh"
        submit_file = "/home/users/wooma/jobs/submit_scripts/sra_debug/" + prefix + ".submit"
        # Sets path to the master shell script that will execute all jobs
        job_master = "/home/users/wooma/jobs/shell_scripts/sra_debug/MASTER.sh"
        # Sets paths to the error and output files for the job
        errorfile = "/home/users/wooma/jobs/error/sra_debug/" + prefix + ".error"
        logfile = "/home/users/wooma/jobs/log/sra_debug/" + prefix + ".log"
        # Sets the path for the SRA toolkit
        SRA_toolkit_path = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/software/sratoolkit.2.8.1-3-centos_linux64/bin/"
        # Sets commands for fastq_dump and gunzip
        fastq_dump = SRA_toolkit_path + "fastq-dump -L 6 -v -v -v -v -v -+ KFS --split-files --gzip -I -O /mnt/lustre1/CompBio/data/immunotherapy/PRJNA307199/ " + file
        sra_stat = SRA_toolkit_path + "sra-stat --quick --xml " + file + " > /mnt/lustre1/CompBio/data/immunotherapy/SRA_stats/" + prefix + "_stats.xml"
        # Writes the shell script
        fh1 = open(shell_script, "w")
        fh1.write("#!/bin/bash\n")
		# CHANGE DIRECTORY
		fh1.write(fastq_dump + "\n")
		fh1.write(sra_stat + "\n")
        fh1.close()
        # Writes the submit file
        fh2 = open(submit_file, "w")
        fh2.write("universe = vanilla\n")
        fh2.write("getenv = true\n")
        fh2.write("executable = " + shell_script + "\n")
        fh2.write("error = " + errorfile + "\n")
        fh2.write("log = " + logfile + "\n")
        fh2.write("queue")
        fh2.close()
        # Appends commands to make shell script executable and submit the submit file to the master shell script
        fh3 = open(job_master, "a")
        fh3.write("chmod u+x " + shell_script + "\n")
        fh3.write("condor_submit " + submit_file + "\n")
        fh3.close()
        
# Initiates master file to spawn jobs
masterfh = open("/home/users/wooma/jobs/shell_scripts/sra_debug/MASTER.sh", "w")
masterfh.write("#!/bin/bash\n")
masterfh.close()

# Generates list of sra files in the PRJNA307199 directory
directory = "/mnt/lustre1/CompBio/data/immunotherapy/PRJNA307199/*.sra"
file_list = glob.glob(directory)

# Writes debugging fastq dump for the files
for file in file_list:
	write_fastqdump_submit(file)
