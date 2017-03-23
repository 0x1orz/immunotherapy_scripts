#!/usr/bin/env python

# Imports and initializes optparse module
import optparse
p = optparse.OptionParser()

# Imports os module
import os

# Adds file1 and file2 options to command line
p.add_option("--err", action="store", dest="error")
p.add_option("--f1", action="store", dest="file1")
p.add_option("--f2", action="store", dest="file2")
p.add_option("--lab", action="store", dest="label")

# Parse command line for files
opts, args = p.parse_args()
error_file = opts.error
r1_file = opts.file1
r2_file = opts.file2
pathtorun = opts.label

# Opens the error file for reading
fh_err = open(error_file, "r")

# Checks whether there were any errors from gunzip -t
# If no, checks to see if spots were equal
if os.stat(error_file).st_size == 0:
	# Opens files for reading
	fh1 = open(r1_file, "r")
	fh2 = open(r2_file, "r")
	# Obtains spots from files
	for line in fh1:
		line = line.strip("/1\n").split()[-1]
		read1_spot = int(line)
	for line in fh2:
		line = line.strip("/2\n").split()[-1]
		read2_spot = int(line)
	# Closes files for reading
	fh1.close()
	fh2.close()
	# Checks for matching spots
	# If they don't match, appends to list of runs where spots don't match
	if read1_spot != read2_spot:
		spotsfh = open("/home/users/wooma/jobs/out/fastq_checks/spot_match_violators.txt", "a")
		spotsfh.write(pathtorun + "\n")
		spotsfh.close()
# If errors from gunzip -t, appends files to list of files with gzip issues
else:
	gzipfh = open("/home/users/wooma/jobs/out/fastq_checks/gzip_violators.txt", "a")
	gzipfh.write(pathtorun + "\n")
	gzipfh.close()
	