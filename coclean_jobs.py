#!/usr/bin/env python

# DBSNP FILE MUST BE SORTED USING PICARD SORT VCF

# Imports and initializes optparse module
import optparse
p = optparse.OptionParser()

# Defines function to write files for submitting co cleaning jobs
def coclean_job(subject, normal, tumor):
	# Sets prefix for output files as subject ID + tumor run accession
	prefix = subject + "." + tumor
	# Sets job files for condor
	shell_script = "/home/users/wooma/jobs/shell_scripts/coclean/" + prefix + ".sh"
	submit_script = "/home/users/wooma/jobs/submit_scripts/coclean/" + prefix + ".submit"
	job_master = "/home/users/wooma/jobs/shell_scripts/coclean/MASTER.sh"	
	errorfile = "/home/users/wooma/jobs/error/coclean/" + prefix + ".error"
	logfile = "/home/users/wooma/jobs/log/coclean/" + prefix + ".log"
	outfile = "/home/users/wooma/jobs/out/coclean/" + prefix + ".out"
	# Sets input bam files
	normal_bam = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + normal + "_recal.bam"
	tumor_bam = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + tumor + "_recal.bam"
	# Sets reference and known variant files
	reference = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/Homo_sapiens_assembly38.fasta"
	dbsnp_file = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/dbsnp_146.hg38.vcf"
	###### MAY NEED TO FIX THESE TWO ######
	indel_file = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf"
	pop_freq = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/hg38/hapmap_3.3.hg38.nochr.vcf"
	# Sets GATK shortcut
	GATK = "java -jar /opt/installed/GATK/GenomeAnalysisTK-3.5.jar"
	# Sets interval file
	intervals = "/mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + prefix + ".intervals"
	# Sets realigned files 
	realigned_normal = normal_bam.strip(".bam") + ".realigned.bam"
	realigned_tumor = tumor_bam.strip(".bam") + ".realigned.bam"
	# Sets commands
	realign_target = GATK + " -T RealignerTargetCreator -R " + reference + " -I " + normal_bam + " -I " + tumor_bam + " --known " + dbsnp_file + " --known " + indel_file + " -o " + intervals
	indel_realign = GATK + " -T IndelRealigner -R " + reference + " -I " + normal_bam + " -I " + tumor_bam + " -nWayOut .realigned.bam --known " + dbsnp_file + " --known " + indel_file + " -targetIntervals " + intervals
	cont_est = GATK + " -T ContEst -R " + reference + " -I:eval " + realigned_tumor + " -I:genotype " + realigned_normal + " --popFile " + pop_freq + " -L " + intervals + " -isr INTERSECTION -o /mnt/lustre1/CompBio/data/immunotherapy/BAM_files/" + prefix + ".contEst.txt"
	# Writes the shell script
	shellfh = open(shell_script, "w")
	shellfh.write("#!/bin/bash\n\n")
	shellfh.write(realign_target + "\n\n")
	shellfh.write(indel_realign + "\n\n")
	shellfh.write(cont_est + "\n\n")
	shellfh.close()
	# Writes the submit file
	submitfh = open(submit_script, "w")
	submitfh.write("universe = vanilla\n")
	submitfh.write("getenv= true\n")
	submitfh.write("request_memory = 50 GB\n")
	submitfh.write("executable = " + shell_script + "\n")
	submitfh.write("error = " + errorfile + "\n")
	submitfh.write("log = " + logfile + "\n")
	submitfh.write("output = " + outfile + "\n")
	submitfh.write("queue")
	submitfh.close()
	# Appends commands to make shell script executable and submit the submit file to the master shell script
	masterfh = open(job_master, "a")
	masterfh.write("chmod u+x " + shell_script + "\n")
	masterfh.write("condor_submit " + submit_script + "\n")
	masterfh.close()	
	
# Adds tn pair file option to command line
p.add_option("-p", action="store", dest="tn_pairs")

# Parse command line for tn pair file
opts, args = p.parse_args()
pair_file = opts.tn_pairs

# Initializes master file to spawn jobs
fh1 = open("/home/users/wooma/jobs/shell_scripts/coclean/MASTER.sh", "w")
fh1.write("#!/bin/bash\n")
fh1.close()

# Opens pair file for reading
pairfh = open(pair_file, "r")

# Loops through file and creates co clean job files for any tumor normal pair
for line in pairfh:
	line = line.strip("\n").split("\t")
	if line[0] != "Subject_ID" and line[1] != "NA":
		subject_id = line[0]
		normal_samp = line[1]
		tumor_samp = line[2]
		coclean_job(subject_id, normal_samp, tumor_samp)
