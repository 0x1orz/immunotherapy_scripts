#!/usr/bin/env python

tn_pairs = "/home/users/wooma/tn_pairs.txt"
fh = open(tn_pairs, "r")

switch_file = "/home/users/wooma/HLA_switching.txt"
switch_fh = open(switch_file, "w")
switch_fh.write("Subject_ID\tNormal\tTumor\n")

for line in fh:
	line = line.strip("\n").split("\t")
	if line[0] != "Subject_ID":
		subject = line[0]
		normal = line[1]
		tumor = line[2]
		if normal != "NA" and tumor != "SRR2588549":
			normal_opt = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/" + normal + "_result.tsv"
			normal_fh = open(normal_opt, "r")
			normal_fh.readline()
			line = normal_fh.readline().strip("\n").split("\t")
			norm_OptA1 = line[1]
			norm_OptA2 = line[2]
			norm_OptB1 = line[3]
			norm_OptB2 = line[4]
			norm_OptC1 = line[5]
			norm_OptC2 = line[6]
			normal_fh.close()
			tumor_opt = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/" + tumor + "_result.tsv"
			tumor_fh = open(tumor_opt, "r")
			tumor_fh.readline()
			line = tumor_fh.readline().strip("\n").split("\t")
			tum_OptA1 = line[1]
			tum_OptA2 = line[2]
			tum_OptB1 = line[3]
			tum_OptB2 = line[4]
			tum_OptC1 = line[5]
			tum_OptC2 = line[6]
			tumor_fh.close()
			match = True
			if norm_OptA1 != tum_OptA1 and norm_OptA1 != tum_OptA2:
				match = False
			if norm_OptA2 != tum_OptA1 and norm_OptA2 != tum_OptA2:
				match = False
			if norm_OptB1 != tum_OptB1 and norm_OptB1 != tum_OptB2:
				match = False
			if norm_OptB2 != tum_OptB1 and norm_OptB2 != tum_OptB2:
				match = False
			if norm_OptC1 != tum_OptC1 and norm_OptC1 != tum_OptC2:
				match = False
			if norm_OptC2 != tum_OptC1 and norm_OptC2 != tum_OptC2:
				match = False
			if match == False:
				switch_line = subject + "\t" + normal + "\t" + tumor + "\n"
				switch_fh.write(switch_line)

switch_fh.close()