#!/usr/bin/env python

import glob

def compare_HLA_calls(optitype_file):
	# Opens optitype file for analysis
	fh_opt = open(optitype_file, "r")
	# Obtains number of lines and returns to beginning of file
	num_lines = sum(1 for line in fh_opt)
	fh_opt.seek(0)
	
	
	# Checks if there is more than 1 result option
	if num_lines > 2:
		# Sets rank weights based on result row
		rank_dict = {'0':2.0, '1':1.75, '2':1.5, '3':1.25, '4':1.0}
		weighted_av_denom  = 0
		for key in rank_dict:
			weighted_av_denom += rank_dict[key]
		# Sets up empty lists to hold all options for each allele
		A = {}
		B = {}
		C = {}
		Aset = []
		Bset = []
		Cset = []
		
		
		# Loops through each line of the file to tally results
		for line in fh_opt:
			line = line.strip("\n").split("\t")
			# Check that line isn't header line
			if line[0] != "":
				# Determines the rank and sets rank value for the line
				rank = line[0]
				rank_value = rank_dict[rank]
				# Determines A1 allele, then sets rank-based score
				A1_allele = line[1]
				A1_allele_score = (rank_value * float(line[9]))
				if A1_allele in A:
					A[A1_allele].append([A1_allele_score, rank_value])
				else:
					A[A1_allele] = [[A1_allele_score, rank_value]]
				# Determines A2 allele, then sets rank-based score
				A2_allele = line[2]
				A2_allele_score = (rank_value * float(line[9]))
				if A2_allele in A:
					A[A2_allele].append([A2_allele_score, rank_value])
				else:
					A[A2_allele] = [[A2_allele_score, rank_value]]
				# Determines A1A2 pair
				Aset.append([A1_allele, A2_allele])
				# Determines B1 allele, then sets rank-based score
				B1_allele = line[3]
				B1_allele_score = (rank_value * float(line[9]))
				if B1_allele in B:
					B[B1_allele].append([B1_allele_score, rank_value])
				else:
					B[B1_allele] = [[B1_allele_score, rank_value]]
				# Determines B2 allele, then sets rank-based score
				B2_allele = line[4]
				B2_allele_score = (rank_value * float(line[9]))
				if B2_allele in B:
					B[B2_allele].append([B2_allele_score, rank_value])
				else:
					B[B2_allele] = [[B2_allele_score, rank_value]]
				# Determines B1,B2 pair
				Bset.append([B1_allele, B2_allele])
				# Determines C1 allele, then sets rank-based score
				C1_allele = line[5]
				C1_allele_score = (rank_value * float(line[9]))
				if C1_allele in C:
					C[C1_allele].append([C1_allele_score, rank_value])
				else:
					C[C1_allele] = [[C1_allele_score, rank_value]]
				# Determines C2 allele, then sets rank-based score
				C2_allele = line[6]
				C2_allele_score = (rank_value * float(line[9]))
				if C2_allele in C:
					C[C2_allele].append([C2_allele_score, rank_value])
				else:
					C[C2_allele] = [[C2_allele_score, rank_value]]
				#Determines C1C2 pair
				Cset.append([C1_allele, C2_allele])
		
		# Takes top call for each allele
		topA1 = Aset[0][0]
		topA2 = Aset[0][1]
		topB1 = Bset[0][0]
		topB2 = Bset[0][1]
		topC1 = Cset[0][0]
		topC2 = Cset[0][1]
		
		# Scoring comparison for all allele options in each allele list
		best_OptAscore = 0
		for key in A:
			num = 0
			denom = 0
			for score in A[key]:
				num += score[0]
				denom += score[1]
			weighted_score = num/denom
			if weighted_score > best_OptAscore:
				best_OptAscore = weighted_score
				OptA1 = key
		allele_pair = next(pair for pair in Aset if OptA1 in pair)
		allele_pair.remove(OptA1)
		OptA2 = allele_pair[0]
						
		best_OptBscore = 0
		for key in B:
			num = 0
			denom = 0
			for score in B[key]:
				num += score[0]
				denom += score[1]
			weighted_score = num/denom
			if weighted_score > best_OptBscore:
				best_OptBscore = weighted_score
				OptB1 = key
		allele_pair = next(pair for pair in Bset if OptB1 in pair)
		allele_pair.remove(OptB1)
		OptB2 = allele_pair[0]

		best_OptCscore = 0
		for key in C:
			num = 0
			denom = 0
			for score in C[key]:
				num += score[0]
				denom += score[1]
			weighted_score = num/denom
			if weighted_score > best_OptCscore:
				best_OptCscore = weighted_score
				OptC1 = key
		allele_pair = next(pair for pair in Cset if OptC1 in pair)
		allele_pair.remove(OptC1)
		OptC2 = allele_pair[0]

	A_mismatch = 0
	B_mismatch = 0
	C_mismatch = 0
	mismatch_list = []
	'''
	# Compares results from top score and weighted score
	if OptA1 != topA1 and OptA1 != topA2 and OptA2 != topA1 and OptA2 != topA2:
		A_mismatch += 2
		mismatch1 = topA1 + "->" + OptA1
		mismatch_list.append(mismatch1)
		mismatch2 = topA2 + "->" + OptA2
		mismatch_list.append(mismatch2)
	elif (OptA1 != topA1 and OptA1 != topA2) and (OptA2 == topA1 or OptA2 == topA2):
		A_mismatch += 1
		if topA1 != topA2:
			allele = next(choice for choice in [topA1, topA2] if choice != OptA2)
		else:
			allele = topA1
		mismatch = allele + "->" + OptA1
		mismatch_list.append(mismatch)
	elif (OptA1 == topA1 or OptA1 == topA2) and (OptA2 != topA1 and OptA2 != topA2):
		A_mismatch += 1
		if topA1 != topA2:
			allele = next(choice for choice in [topA1, topA2] if choice != OptA1)
		else:
			allele = topA1
		mismatch = allele + "->" + OptA2
		mismatch_list.append(mismatch)	

	if OptB1 != topB1 and OptB1 != topB2 and OptB2 != topB1 and OptB2 != topB2:
		B_mismatch += 2
		mismatch1 = topB1 + "->" + OptB1
		mismatch_list.append(mismatch1)
		mismatch2 = topB2 + "->" + OptB2
		mismatch_list.append(mismatch2)
	elif (OptB1 != topB1 and OptB1 != topB2) and (OptB2 == topB1 or OptB2 == topB2):
		B_mismatch += 1
		if topB1 != topB2:
			allele = next(choice for choice in [topB1, topB2] if choice != OptB2)
		else:
			allele = topB1
		mismatch = allele + "->" + OptB1
		mismatch_list.append(mismatch)
	elif (OptB1 == topB1 or OptB1 == topB2) and (OptB2 != topB1 and OptB2 != topB2):
		B_mismatch += 1
		if topB1 != topB2:
			allele = next(choice for choice in [topB1, topB2] if choice != OptB1)
		else:
			allele = topB1
		mismatch = allele + "->" + OptB2
		mismatch_list.append(mismatch)	
		
	if OptC1 != topC1 and OptC1 != topC2 and OptC2 != topC1 and OptC2 != topC2:
		C_mismatch += 2
		mismatch1 = topC1 + "->" + OptC1
		mismatch_list.append(mismatch1)
		mismatch2 = topC2 + "->" + OptC2
		mismatch_list.append(mismatch2)
	elif (OptC1 != topC1 and OptC1 != topC2) and (OptC2 == topC1 or OptC2 == topC2):
		C_mismatch += 1
		if topC1 != topC2:
			allele = next(choice for choice in [topC1, topC2] if choice != OptC2)
		else:
			allele = topC1
		mismatch = allele + "->" + OptC1
		mismatch_list.append(mismatch)
	elif (OptC1 == topC1 or OptC1 == topC2) and (OptC2 != topC1 and OptC2 != topC2):
		C_mismatch += 1
		if topC1 != topC2:
			allele = next(choice for choice in [topC1, topC2] if choice != OptC1)
		else:
			allele = topC1
		mismatch = allele + "->" + OptC2
		mismatch_list.append(mismatch)		

	'''
	if (OptA1 and OptA2) not in [topA1, topA2]:
		A_mismatch += 2
	elif (OptA1 or OptA2) not in [topA1, topA2]:
		A_mismatch += 1
		
	if (OptB1 and OptB2) not in [topB1, topB2]:
		B_mismatch += 2
	elif (OptB1 or OptB2) not in [topB1, topB2]:
		A_mismatch += 1
	
	if (OptC1 and OptC2) not in [topC1, topC2]:
		C_mismatch += 2
	elif (OptC1 or OptC2) not in [topC1, topC2]:
		C_mismatch += 1

	if (A_mismatch or B_mismatch or C_mismatch) == 1:
		print optitype_file
	return [str(A_mismatch), str(B_mismatch), str(C_mismatch), mismatch_list]


# Creates a string for the result.tsv files in the directory to search and compiles those files
search_directory = "/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/*result.tsv"
directory_files = glob.glob(search_directory)
directory_files.remove("/mnt/lustre1/CompBio/data/immunotherapy/HLA_typing/_EGAR00001418719_18468_4_3_result.tsv")

# Dictionaries to hold results with 0, 1, or 2 matches
A_matches = {"0" : 0, "1" : 0 , "2" : 0}
B_matches = {"0" : 0, "1" : 0 , "2" : 0}
C_matches = {"0" : 0, "1" : 0 , "2" : 0}
allele_mismatches = {}

# Compares HLA_calls for each file
for file in directory_files:
	results = compare_HLA_calls(file)
	A_count = results[0]
	A_matches[A_count] += 1
	B_count = results[1]
	B_matches[B_count] += 1
	C_count = results[2]
	C_matches[C_count] += 1
	mismatches = results[3]
	for item in mismatches:
		if item in allele_mismatches:
			allele_mismatches[item] += 1
		else:
			allele_mismatches[item] = 1


'''
alleles_switched = {}

top2weighted = "top_to_weighted_switches.txt"
top2w_fh = open(top2weighted, "w")
top2w_fh.write("Allele_switch\tCount\n")

for key in allele_mismatches:
	if allele_mismatches[key] > 1:
		line = key + "\t" + str(allele_mismatches[key]) + "\n"
		top2w_fh.write(line)
	switched_allele = key.split("->")[0]
	if switched_allele in alleles_switched:
		alleles_switched[switched_allele] += 1
	else:
		alleles_switched[switched_allele] = 1

top2w_fh.close()

common_alleles = "common_top_alleles_switched.txt"
common_fh = open(common_alleles, "w")
common_fh.write("Switched_allele\tCount\n")


for key in alleles_switched:
	if alleles_switched[key] > 1:
		line = key + "\t" + str(alleles_switched[key]) + "\n"
		common_fh.write(line)

common_fh.close()

mismatch_file = "allele_mismatches.txt"
mismatch_fh = open(mismatch_file, "w")
mismatch_fh.write("Allele_type\tCount_0_mismatches\tCount_1_mismatch\tCount_2_mismatches\n")
Aline = ("A\t" + str(A_matches["0"]) + "\t" + str(A_matches["1"]) + "\t" + str(A_matches["2"]) + "\n")
Bline = ("B\t" + str(B_matches["0"]) + "\t" + str(B_matches["1"]) + "\t" + str(B_matches["2"]) + "\n")
Cline = ("C\t" + str(C_matches["0"]) + "\t" + str(C_matches["1"]) + "\t" + str(C_matches["2"]) + "\n")
mismatch_fh.write(Aline)
mismatch_fh.write(Bline)
mismatch_fh.write(Cline)
mismatch_fh.close()
'''


print A_matches
print B_matches
print C_matches
print allele_mismatches
