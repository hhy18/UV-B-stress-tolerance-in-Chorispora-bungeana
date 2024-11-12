"""
1. 使用R包clusterprofile做非模式KEGG富集分析时，使用的输入自定义kegg注释文件格式为：
	geneID	    Pathway	    Path_Description
	1			ko:00001	spindle
	2			ko:00002	mitotic spindle
	3			ko:00003	kinetochore
2. 使用的ko-description 为 FLS下载的注释文件
3. 本脚本使用K输出对应的所有ko及其description
"""

import re
import sys
import os 
import time

def main(kaas_file):
	file = "/data/01/user102/hhy/piplines/clusterProfiler/KEGG/ko00001.keg"
	
	# 分割行号
	ko_list = list()
	contents = list()
	# 按照C分割，记录行号
	for lines in open(file).readlines():
		if lines.startswith("C") or lines.startswith("D"):
			contents.append(lines)
	
	for index,lines in enumerate(contents):
		if lines.startswith("C"):
			ko_list.append(index)
	
	ko_list.append(len(contents)-1)
	
	# 启动标记
	start = 0
	end = len(ko_list)
	total_list = list()
	
	# 遍历每个分割部分
	while start+1 < end:
		sub_dict = dict()
		
		ko_name = "ko"+re.search(r"^C\s+(\d+)\s+(.*)\s+",contents[ko_list[start]]).group(1)
		ko_description = re.search(r"^C\s+(\d+)\s+(.*)\s+",contents[ko_list[start]]).group(2)
		sub_dict[(ko_name,ko_description)] = []
		
		for index,i in enumerate(contents[ko_list[start]:ko_list[start+1]]):
			if i.startswith("D"):
				K_name = i.strip().split()[1]
				sub_dict[(ko_name,ko_description)].append(K_name)
		
		# 进入下个循环
		total_list.append(sub_dict)
		start +=1

	
	with open(kaas_file) as inf:
		for lines in inf.readlines():
			flag = 1
			line = lines.strip().split()
			
			if len(line) == 2:
				for i in total_list:
					for k,v in i.items():
						if line[1] in v:
							ko_self = k[0]
							ko_description = k[1]
							print("\t".join([line[0],ko_self,ko_description]))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("python %s kaas_annotation"%sys.argv[0])
		print("kaas_annotation--kaas注释结果")
		sys.exit(0)		
	main(sys.argv[1])

