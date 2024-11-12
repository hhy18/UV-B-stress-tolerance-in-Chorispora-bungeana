# 获取差异表达基因表达量

import re
import os 
import sys

def main(DEG_res,gene_fpkm):
	gene_label = list()
	with open(DEG_res) as inf:
		for lines in inf.readlines():
			gene_label.append(lines.strip())

	with open(gene_fpkm) as inf:
			for index,lines in enumerate(inf.readlines()):
				if index > 0:
					line = lines.strip().split(",")
					if line[0].rstrip(r"\.1") in gene_label:
						print(lines,end="")
				else:
					print(lines,end="")

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("python %s DEG_res gene_fpkm"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1],sys.argv[2])