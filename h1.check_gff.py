"""
1. 新疆杨基因组注释文件报错提出id重复,检查gff文件的重复信息
"""

import re
import sys
import os 

def main(infile):
	list1 = list()
	with open(infile) as inf:
		for lines in inf.readlines():
			if not lines.startswith("#") and lines != "\n":
				if lines not in list1:
					list1.append(lines)
					print(lines,end="")
				else:
					# print("Error",lines)
					pass
	# for i in list1:
	# 	print(i)

main(sys.argv[1])
