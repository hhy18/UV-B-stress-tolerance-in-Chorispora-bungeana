"""
从interproscan注释结果中，取回注释的基因的GO号
"""

import re
import sys
import os

def main(file):

	go_dict = dict()
	with open(file) as inf:
		for lines in inf.readlines():
			line = lines.strip().split("\t")
			goid = re.findall(r"GO:\d+",lines)
			if line[0] not in go_dict:
				go_dict[line[0]] = []
			for i in goid:
				go_dict[line[0]].append(i)

	for k,v in go_dict.items():
		if v:
			print(k+"\t"+"\t".join(v))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("python %s interproscan_out"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1])

