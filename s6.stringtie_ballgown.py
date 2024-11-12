"""
1. 执行stringtie 定量分析 ballgown
"""

import re
import sys
import os 


def main(sortbam_dir,outdir,merge_gtf):
	sortbam_dir = os.path.abspath(sortbam_dir)
	outdir = os.path.abspath(outdir)
	merge_gtf = os.path.abspath(merge_gtf)

	for file in os.listdir(sortbam_dir):
		if file.endswith("sort.bam"):
			full_bam = os.path.join(sortbam_dir,file)
			file_name = re.sub(r"\.sort\.bam","",file)
			print("stringtie -e -B -p 8 -G {merge_gtf} -o {outdir}/{file_name}_ballgown/output_merge.gtf {full_bam}".format(outdir=outdir,merge_gtf=merge_gtf,file_name=file_name,full_bam=full_bam))

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("使用preDE.py 转换为radcount 矫正用于差异表达分析")
		print("Python %s sortbam_dir outdir merge_gtf"%sys.argv)
		print("sortbam_dir--sort.bam文件夹")
		print("outdir--定量结果输出文件夹")
		print("merge_gtf--merge_gtf文件位置")
		sys.exit(0)

	main(sys.argv[1],sys.argv[2],sys.argv[3])