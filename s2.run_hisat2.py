"""
1. 运行histat2
"""
import re
import sys
import os 

def main(indir,index,outdir):
	outdir = os.path.abspath(outdir)
	indir = os.path.abspath(indir)
	pre_list = set()
	for file in os.listdir(indir):
		file_pre = re.sub(r"(_\d.fq.gz)","",file)
		pre_list.add(file_pre)

	for i in pre_list:
		R1 = os.path.join(indir,i+"_1.fq.gz")
		R2 = os.path.join(indir,i+"_2.fq.gz")
		print("hisat2 -p 10 -x {index} -1 {R1} -2 {R2} -S {outdir}/{i}.sam".format(index=index,R1=R1,R2=R2,i=i,outdir=outdir))

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("python %s indir index outdir"%sys.argv[0])
		sys.exit(0)

	main(sys.argv[1],sys.argv[2],sys.argv[3])

