"""
1. 为clusterprofile进行GO富集分析，准备输入文件
2. 获得本脚本的输入文件，可以使用脚本s11.get_goid_from_interproscan.py整理interproscan结果
"""

import re
import sys
import os 

def main(go_annotation):
	
	term2name = "/data/00/user/user102/hhy/piplines/clusterProfiler/GO/script/term2name.txt"
	# term2name = "/data/00/user/user102/hhy/piplines/clusterProfiler/GO/data/term2name.csv"
	term2name_dict = dict()
	with open(term2name) as inf:
		for lines in inf.readlines():
			line = lines.strip().split(",")
			term2name_dict[line[0]] = line[1]

	with open(go_annotation) as inf:
		for lines in inf.readlines():
			line = lines.strip().split("\t")
			if line != 1:
				for go in line[1:]:
					print("\t".join([line[0],go,term2name_dict[go]]))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("python %s go_annotation\ngo_annotation--整理好的基因GO注释结果"%sys.argv[0])
		sys.exit(0)

	main(sys.argv[1])

