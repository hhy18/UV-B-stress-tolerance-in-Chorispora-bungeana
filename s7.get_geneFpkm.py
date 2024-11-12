"""
1. 从stringtie ballgown 中产生的样品注释文件中提取转录本的表达量
"""

import re
import os 
import sys

def main(indir):
	indir = os.path.abspath(indir)

	file_list = list()
	fpkm_dict = dict()
	for dirpath,dirname,files in os.walk(indir):
		for file in files:
			if file == "output_merge.gtf":
				full_file = os.path.join(dirpath,file)
				file_list.append(os.path.basename(os.path.dirname(full_file)))
				
				with open(full_file) as inf:
					for lines in inf.readlines():
						if lines.startswith("#"): continue
						line = lines.strip().split("\t")
						if line[2] == "transcript":
							transcript_id = re.search(r"transcript_id\s+\"(.*?)\";",line[-1]).group(1)
							fpkm = re.search(r"TPM\s+\"(.*?)\";",line[-1]).group(1)
							if transcript_id not in fpkm_dict:
								fpkm_dict[transcript_id] = []

							fpkm_dict[transcript_id].append(fpkm) 

	print("geneid"+","+",".join(file_list))
	for k,v in fpkm_dict.items():
		if sum(map(float,v))/len(v) >= 1:
			print(k+","+",".join(v))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("python %s ballgown_dir\nballgown_dir--ballgown产生总文件夹"%sys.argv[0])
		sys.exit(0)

	main(sys.argv[1])