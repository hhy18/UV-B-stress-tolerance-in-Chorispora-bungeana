# 鉴定各个时间点之间的上调和下调数量

import re
import os 
import sys

def main(indir):

	for file in os.listdir(indir):
		if file.endswith("DEG.txt"):
			fullfile = os.path.join(indir,file)

			all_DEG = list()
			up_DEG = list()
			down_DEG = list()
			with open(fullfile) as inf:
				for index,lines in enumerate(inf.readlines()):
					if index > 0:
						line = lines.strip().split()
						if abs(float(line[2]))>=1 and float(line[6]) < 0.05:
							all_DEG.append(line[0])
						if float(line[2]) >= 1 and float(line[6]) < 0.05:
							up_DEG.append(line[0])
						if float(line[2]) <= -1 and float(line[6]) < 0.05:
							down_DEG.append(line[0])

			print(f"{fullfile} all_DEG:{len(all_DEG)}")
			print(f"{fullfile} up_DEG:{len(up_DEG)}")
			print(f"{fullfile} down_DEG:{len(down_DEG)}")
			print("="*40)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("python %s deseq_dir"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1])