"""
将全基因组重测序二代数据进行过滤，使用软件为fastp
"""

import re
import os 
import sys

def main(indir, outdir):
	indir = os.path.abspath(indir)
	outdir = os.path.abspath(outdir)

	sample_list = list()
	for file in os.listdir(indir):
		if file.endswith("gz"):
			#sample = re.search(r"(LD_\d{1,}_\d{1,})",file).group(1)
			# print(sample)
			sample = re.sub(r"_\d{1}.fq.gz","",file)
			sample_list.append(sample)

	sample_list = list(set(sample_list))
	for sample in sample_list:
		html = os.path.join(outdir,sample+".html")

		r1 = os.path.join(indir,sample+"_1.fq.gz")
		r2 = os.path.join(indir,sample+"_2.fq.gz")
		
		o1 = os.path.join(outdir,sample+"_1.fastp.fq.gz")
		o2 = os.path.join(outdir,sample+"_2.fastp.fq.gz")
		
		params = "--compression=6 --thread=5 --length_required=50 --n_base_limit=5 -Q"
		print("fastp {params} -i {r1} -o {o1} -I {r2} -O {o2} -h {html}".format(params=params, r1=r1, o1=o1, r2=r2, o2=o2, html=html))

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("python %s indir outdir"%sys.argv[0])
		sys.exit(0)

	main(sys.argv[1],sys.argv[2])
