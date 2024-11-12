"""
1. 从所有的差异表达序列中获得基因id
"""

import re
import os 
import sys
from Bio import SeqIO

def main(all_fa):
	for seq in SeqIO.parse(all_fa,"fasta"):
		print(seq.id)


main(sys.argv[1])