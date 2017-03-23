#!/usr/bin/env python


file = "/mnt/lustre1/CompBio/projs/RThompson/immunotherapy/IMMUNOTHERAPY_SAMPLE_KEY.txt"
fh = open(file, "r")

tumor_wes = {}
normal_wes = {}
tumor_rna = {}

for line in fh:
	line = line.strip("\n").split("\t")
	if line[0] != "subject_id" and "PRJNA265091" not in line[0]:
		subject_id = line[0]
		tn_status = line [15]
		location = line[16]
		run = line[31]
		seq_type = line[34]
		if tn_status == "T" and seq_type == "WES":
			if subject_id not in tumor_wes:
				tumor_wes[subject_id] = [[run, location]]
			else:
				tumor_wes[subject_id].append([run, location])
		elif tn_status == "N" and seq_type == "WES":
			if subject_id not in normal_wes:
				normal_wes[subject_id] = [[run, location]]
			else:
				normal_wes[subject_id].append([run, location])
		elif tn_status == "T" and seq_type == "RNA-seq":
			if subject_id not in tumor_rna:
				tumor_rna[subject_id] = [[run, location]]
			else:
				tumor_rna[subject_id].append([run, location])

fh.close()

# PGDX not incorporated because we don't have info on them

pairs_file = "/home/users/wooma/tn_pairs.txt"
pairs_fh = open(pairs_file, "w")
pairs_fh.write("Subject_ID\tNormal_sample\tTumor_sample\tRNA_sample\n")

for subject in tumor_wes:
	for tumor_sample in tumor_wes[subject]:
		tumor_run = tumor_sample[0]
		location = tumor_sample[1]
		if subject in normal_wes:
			normal_run = normal_wes[subject][0][0]
		else:
			normal_run = "NA"
		if subject in tumor_rna:
			for rna_sample in tumor_rna[subject]:
				if rna_sample[1] == location:
					rna_run = rna_sample[0]
					tumor_rna[subject].remove(rna_sample)
					if len(tumor_rna[subject]) == 0:
						del tumor_rna[subject]
		else:
			rna_run = "NA"
		line = subject + "\t" + normal_run + "\t" + tumor_run + "\t" + rna_run + "\n"
		pairs_fh.write(line)

print tumor_rna

# Have a few straggler RNA samples

pairs_fh.close()