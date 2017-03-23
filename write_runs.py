#!/usr/bin/env python

root = "SRR36539"
fh = open("PRJNA324705_runs.txt", "w")

for i in range(52, 65):
	run = root + str(i)
	fh.write(run + "\n")