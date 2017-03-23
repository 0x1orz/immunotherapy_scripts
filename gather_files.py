#!/usr/bin/env python

# Imports glob and os modules
import glob
import os

# Creates a list of all subdirectory and file names in the immunotherapy directory
directory_list = os.listdir("/mnt/lustre1/CompBio/data/immunotherapy/")

# Removes the single file from the list of items in the immunotherapy directory
directory_list.remove(directory_list[6])

fh = open("/home/users/wooma/all_files.txt", "w")

for directory in directory_list:
	path = "/mnt/lustre1/CompBio/data/immunotherapy/" + directory + "/*"
	files = glob.glob(path)
	for file in files:
		fh.write(file + "\n")
