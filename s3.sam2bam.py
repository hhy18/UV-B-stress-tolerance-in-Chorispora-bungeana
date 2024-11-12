"""
1. 将目录下的所有sam文件转为bam文件
"""
import re
import sys
import os 

def main(indir):
	indir=os.path.abspath(indir)
	for file in os.listdir(indir):
		if file.endswith("sam"):
			full = os.path.join(indir,file)
			sam = full
			bam = re.sub("sam","bam",sam)
			print("samtools view -bS {sam} > {bam}".format(sam=sam,bam=bam))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("python %s indir"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1])