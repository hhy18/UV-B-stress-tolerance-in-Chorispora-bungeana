"""
1. 获得genelist
"""

import re
import sys
import os 

def main(gtf):
	with open(gtf) as inf:
		for lines in inf.readlines():
			line = lines.strip().split("\t")
			if line[2] == "mRNA":
				geneid = re.search("ID=(.*?);",line[-1]).group(1)
				print(geneid)

main(sys.argv[1])