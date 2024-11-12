# 数据整理为差异表达基因图谱

import re
import os
import sys
import pandas as pd 

def main(all_fpkm,DEG_res):
	data = pd.read_csv(all_fpkm,header=0)
	df = data.reindex(columns=["geneid", "CK-Q-1A_ballgown", "CK-Q-2A_ballgown", "CK-Q-3A_ballgown", "CK-Q-4A_ballgown", "0.5-Q-1A_ballgown", "0.5-Q-2A_ballgown", "0.5-Q-3A_ballgown", "0.5-Q-4A_ballgown", "1-Q-1A_ballgown", "1-Q-2A_ballgown", "1-Q-3A_ballgown", "1-Q-4A_ballgown", "3-Q-1A_ballgown", "3-Q-2A_ballgown", "3-Q-3A_ballgown", "3-Q-4A_ballgown", "6-Q-1A_ballgown", "6-Q-2A_ballgown", "6-Q-3A_ballgown", "6-Q-4A_ballgown", "12-Q-1A_ballgown", "12-Q-2A_ballgown", "12-Q-3A_ballgown", "12-Q-4A_ballgown"])
	df.to_csv(f"{all_fpkm.rstrip('.txt')}.reindex.txt",index=False)

	gene_fpkm = dict()
	header = None
	with open(f"{all_fpkm.rstrip('.txt')}.reindex.txt") as inf:
		for index, lines in enumerate(inf.readlines()):
			if index == 0:
				header = lines.strip().split(",")
			else:
				line = lines.strip().split(",")
				gene_fpkm[line[0]]=line

	header.insert(1,"log2FC")
	print(",".join(header))

	with open(DEG_res) as inf:
		for index, lines in enumerate(inf.readlines()):
			if index > 0:
				line = lines.strip().split()
				geneid = eval(line[0])+".1"
				log2FC = line[2]

				if geneid in gene_fpkm:
					new_line = gene_fpkm[geneid]
					new_line.insert(1,log2FC)
					print(",".join(new_line))
				# print(",".join(new_line))



main(sys.argv[1],sys.argv[2])

