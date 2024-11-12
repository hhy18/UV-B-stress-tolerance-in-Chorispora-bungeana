# 数据整理为差异表达基因图谱, log2FC变化

import re
import os
import sys
import pandas as pd


def pro_a(file,num):
	with open(file) as inf:
			for index,lines in enumerate(inf.readlines()):
				if index > 0:
					line = lines.strip().split()
					line[0] = eval(line[0]) + ".1"
					if line[0] in all_gene_dict:
						# if float(line[2]) > 10:
						# 	line[2] = 10
						# if float(line[2]) < -10:
						# 	line[2] = -10
						all_gene_dict[line[0]][num]=float(line[2])

def main(all_fpkm,DEG_res1,DEG_res2,DEG_res3,DEG_res4):
	global all_gene_dict
	all_gene_dict = dict()

	with open(all_fpkm) as inf:
		for index,lines in enumerate(inf.readlines()):
			if index > 0:
				line = lines.strip().split(",")
				all_gene_dict.setdefault(line[0],[0,0,0,0])

	pro_a(DEG_res1,0)
	pro_a(DEG_res2,1)
	pro_a(DEG_res3,2)
	pro_a(DEG_res4,3)
	# pro_a(DEG_res5,4)
	
	all_line = list()
	for k,v in all_gene_dict.items():
		if all([float(i) == 0 for i in v]):
			continue
		v = list(map(float,v))
		v.insert(0,k)
		all_line.append(v)

	print(",".join(["geneid","CK_1","CK_3","CK_6","CK_12"]))
	for i in all_line:
		print(",".join(map(str,i)))

	# df = pd.DataFrame(all_line,columns=["geneid","CK_1","CK_3","CK_6","CK_12"])
	# df = df.sort_values(by="CK_1")
	# df.to_csv("hua_DEG.logFC.csv",index=False)

main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

