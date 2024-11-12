# 因为每个样本有4个处理，所以我们只保留三个值相近的值
import re
import os
import sys

def find_closest_values(lst):
	lst = list(map(float,lst))
	sorted_lst = sorted(lst, reverse=True)
	largest_values = sorted_lst[:3]
	return largest_values

def main(tpm):
	gene_tpm = dict()
	with open(tpm) as inf:
		for index,lines in enumerate(inf.readlines()):
			if index > 0:
				line = lines.strip().split(",")
				CK_res = find_closest_values(line[1:5])
				h_05 = find_closest_values(line[9:13])
				h_1 = find_closest_values(line[13:17])
				h_3 = find_closest_values(line[17:21])
				h_6 = find_closest_values(line[17:21])
				h_12 = find_closest_values(line[21:25])

				gene_tpm[line[0]]={"CK":CK_res,
						"h_0.5":h_05,
						"h_1":h_1,
						"h_3":h_3,
						"h_6":h_6,
						"h_12":h_12}

	for k,v in gene_tpm.items():
		print(k+",",[i for i in v.values()])

if __name__ == '__main__':
	main(sys.argv[1])



