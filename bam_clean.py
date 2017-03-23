#!/usr/bin/env python

# DBSNP FILE MUST BE SORTED USING PICARD SORT VCF

# Imports glob module
import glob

def clean_bam_job(bamfile):
	# Obtains the run name from the bam file path
	run = bamfile.strip(".bam").split("/")[-1]
	# Sets paths to shell, submit, and master scripts for job
	shell_script = "/home/users/wooma/jobs/shell_scripts/bam_cleaning/" + run + ".sh"
	submit_script = "/home/users/wooma/jobs/submit_scripts/bam_cleaning/" + run + ".submit" 
	job_master = "/home/users/wooma/jobs/shell_scripts/bam_cleaning/MASTER.sh"
	# Sets paths to error, log, and outfiles for job
	errorfile = "/home/users/wooma/jobs/error/bam_cleaning/" + run + ".error" 
	logfile = "/home/users/wooma/jobs/log/bam_cleaning/" + run + ".log"
	outputfile = "/home/users/wooma/jobs/out/bam_cleaning/" + run + ".out"
	# Sets paths to picard and GATK ~tools
	picard_tool = "java -jar /opt/installed/picard/picard-tools-1.110/"
	GATK_tool = "java -jar /opt/installed/GATK/GenomeAnalysisTK-3.5.jar"
	# Sets path to reference genome
	reference = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/Homo_sapiens_assembly38.fasta"
	dbsnp_file = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/dbsnp_146.hg38.vcf"
	# Sets output file names
	sort_file = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + run + "_sorted.bam"
	dup_file = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + run + "_marked.bam"
	metrics_file = "/mnt/lustre1/CompBio/data/immunotherapy/duplicate_metrics/" + run + "_metrics.txt"
	recal_report = "/mnt/lustre1/CompBio/data/immunotherapy/recalibration_reports/" + run + "_recalibration_report.grp"
	recal_file = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + run + "_recal.bam"
	# Sets mark duplicates base recalibration commands
	sort_sam = picard_tool + "AddOrReplaceReadGroups.jar I=" + bamfile + " O=" + sort_file + " SORT_ORDER=coordinate RGLB=foo RGPL=Illumina RGPU=bar RGSM=" + run
	mark_dups = picard_tool + "MarkDuplicates.jar I=" + sort_file + " O=" + dup_file + " M=" + metrics_file
	index = picard_tool + "BuildBamIndex.jar I=" + dup_file
	base_recal = GATK_tool + " -T BaseRecalibrator -R " + reference + " -I " + dup_file + " -knownSites " + dbsnp_file + " -o " + recal_report
	base_q_recal = GATK_tool + " -T PrintReads -R " + reference + " -I " + dup_file + " -BQSR " + recal_report + " -o " + recal_file 
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n")
	shellfh.write(sort_sam + "\n")
	shellfh.write(mark_dups + "\n")
	shellfh.write(index + "\n")
	shellfh.write(base_recal + "\n")
	shellfh.write(base_q_recal + "\n")
	shellfh.close()
	# Writes the submit file
	submitfh = open(submit_script, "w")
	submitfh.write("universe = vanilla\n")
	submitfh.write("getenv= true\n")
	submitfh.write("request_memory = 50 GB\n")
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
fh1 = open("/home/users/wooma/jobs/shell_scripts/bam_cleaning/MASTER.sh", "w")
fh1.write("#!/bin/bash\n")
fh1.close()

# Creates a string for the directory to search
directory = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/*.bam"

# Obtains list of read 1 files in the directory
directory_files = glob.glob(directory)

for file in directory_files:
	if "marked" not in file and "sorted" not in file and "recal" not in file:
		clean_bam_job(file)
