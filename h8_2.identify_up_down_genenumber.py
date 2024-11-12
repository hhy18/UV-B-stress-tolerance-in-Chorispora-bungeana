# 鉴定各个时间点之间的上调和下调数量,多少同源和特异

import re
import os 
import sys

def main(indir,mapid_file):
	map_id = dict()
	with open(mapid_file) as inf:
		for lines in inf.readlines():
			line = lines.strip().split()
			map_id[line[1]] = line[2]


	for file in os.listdir(indir):
		if file.endswith("DEG.txt"):
			fullfile = os.path.join(indir,file)

			all_DEG = list()
			up_DEG = list()
			down_DEG = list()
			up_DEG_homo = list()
			down_DEG_homo = list()
			all_DEG_homo = list()

			with open(fullfile) as inf:
				for index,lines in enumerate(inf.readlines()):
					if index > 0:
						line = lines.strip().split()
						if abs(float(line[2]))>=1 and float(line[6]) < 0.05:
							all_DEG.append(line[0])
							if eval(line[0])+".1" in map_id:
								all_DEG_homo.append(line[0])
						
						if float(line[2]) >= 1 and float(line[6]) < 0.05:
							up_DEG.append(line[0])
							if eval(line[0])+".1" in map_id:
								up_DEG_homo.append(line[0])

						if float(line[2]) <= -1 and float(line[6]) < 0.05:
							down_DEG.append(line[0])
							if eval(line[0])+".1" in map_id:
								down_DEG_homo.append(line[0])

			print(f"{fullfile} all_DEG:{len(all_DEG)}")
			print(f"{fullfile} all_DEG_homo:{len(all_DEG_homo)}")
			print(f"{fullfile} up_DEG:{len(up_DEG)}")
			print(f"{fullfile} up_DEG_homo:{len(up_DEG_homo)}")
			print(f"{fullfile} down_DEG:{len(down_DEG)}")
			print(f"{fullfile} down_DEG_homo:{len(down_DEG_homo)}")

			print("="*40)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("python %s deseq_dir mapid_file"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1],sys.argv[2])