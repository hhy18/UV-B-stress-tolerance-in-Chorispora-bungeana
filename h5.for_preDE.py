# gtf文件用于preDE

import re
import os
import sys

def main(indir):
	indir = os.path.abspath(indir)
	for file in os.listdir(indir):
		if file.endswith("gtf"):
			fullfile = os.path.join(indir,file)
			name = file.strip(".gtf")
			print("\t".join([name,fullfile]))

main(sys.argv[1])