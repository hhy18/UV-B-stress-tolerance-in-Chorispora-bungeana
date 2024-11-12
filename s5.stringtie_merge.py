"""
1. 执行stringtie merge 操作并进行定量
2. 根据输入目录下的*gtf生成sample_list.txt
3. 执行merge操作获得merge后的gtf
4. 根据合并的注释文件进行定量
"""

import re
import sys
import os 


def main(gtf_dir,refgtf):
	gtf_dir = os.path.abspath(gtf_dir)
	# print(gtf_dir)

	with open(gtf_dir+"/sample_list.txt","w") as ouf:
		for file in os.listdir(gtf_dir):
			if file.endswith("gtf"):
				full = os.path.join(gtf_dir,file)
				print(full,file=ouf)
	
	if os.path.exists(gtf_dir+"/sample_list.txt"):
		print("stringtie --merge -p 10 -G {refgtf}  -o {gtf_dir}/stringtie_merged.gtf {gtf_dir}/sample_list.txt".format(refgtf=refgtf,gtf_dir=gtf_dir))

	
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("python %s gtf_dir refgtf\ngtf_dir--stringtie生成gtf文件夹\nrefgtf--参考基因组注释文件"%sys.argv[0])
		sys.exit(0)
	main(sys.argv[1],sys.argv[2])
