# 获取差异表达基因列表
# selectresult=subset(res,(log2FoldChange > 1|-log2FoldChange>1)&padj<0.05)

import re
import os 
import sys

def main(file_dir):
	DEG_all_list = set()
	for file in os.listdir(file_dir):
		if file.endswith("DEG.txt"):	
			with open(file) as inf, open(f"{file}.genelist","w") as ouf:
				for index,lines in enumerate(inf.readlines()):
					if index > 0:
						line = lines.strip().split()
						gene = eval(line[0])
						print(gene,file=ouf)
						DEG_all_list.add(gene)

	for i in DEG_all_list:
		print(i)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("python %s DEG_file_indir"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1])