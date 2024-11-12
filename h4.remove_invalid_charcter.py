"""
1. 因为interproscan 不能识别序列中的.和*代表的终止密码子，所以需要去除序列中的这些特殊字符
"""

import re
import os 
import sys 
from Bio import SeqIO

def main(file):
	for seq in SeqIO.parse(file,"fasta"):
		newseq = re.sub(r"[^a-zA-Z0-9]","",str(seq.seq))
		print(">"+seq.id+"\n"+newseq)


main(sys.argv[1])