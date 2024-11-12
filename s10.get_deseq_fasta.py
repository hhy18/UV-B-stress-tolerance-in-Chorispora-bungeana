"""
1. 将deseq2获得的差异表达基因按照geneid，提取该基因的序列用于后续的GO注释
"""

import re
import sys
import os 
from Bio import SeqIO


def main(ref_pro,deseq_file):
	deseq_file = os.path.abspath(deseq_file)
	ref_pro = os.path.abspath(ref_pro)

	seq_dict = dict()
	for seq in SeqIO.parse(ref_pro,"fasta"):
		origid = re.search(r"OriTrascriptID=(.*?)\s+",seq.description).group(1)
		seq_dict[origid] = seq.seq

	with open(deseq_file) as inf:
		for index,lines in enumerate(inf.readlines()):
			if not lines.startswith("#") and index > 0:
				line = lines.strip().split()
				seqid = eval(line[0])
				print(">"+seqid+"\n"+seq_dict[seqid])

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("python %s ref_pro deseq_file"%sys.argv)
		sys.exit(0)
	main(sys.argv[1],sys.argv[2])
				

