"""
1. 寻找目录下的bam文件，批量化运行stringtie
"""

import os
import re
import sys

def main(indir,outdir,refgff):
	indir = os.path.abspath(indir)
	outdir = os.path.abspath(outdir)

	for file in os.listdir(indir):
		if file.endswith("bam"):
			bam = os.path.join(indir,file)
			sortbam = re.sub("bam","sort.bam",bam)
			gtf = re.sub("bam","gtf",file)
			print("samtools sort {bam} -o {sortbam}; stringtie -p 10 -e -G {refgff}  -o {outdir}/{gtf} {sortbam}".format(bam=bam,sortbam=sortbam,refgff=refgff,gtf=gtf,outdir=outdir))

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("python %s indir outdir refgff"%sys.argv[0])
		sys.exit(0)

	main(sys.argv[1],sys.argv[2],sys.argv[3])
