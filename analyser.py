import collections
import math
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import sys

def check_for_arguments(arguments):
	if(len(arguments) < 3 or len(arguments) > 3):
		print "Please provide two arguments: The .orig file and .alt file."

		sys.exit()

def read_file(file_path):
	with open(file_path) as f:
		file_contents = f.readlines()
	
	return [file_line.strip()[0:8] for file_line in file_contents]

def hex_to_binary(content):
	return [bin(int(hex_data, 16))[2:].zfill(8) for hex_data in content]

def collisions(content):
	content_counter = collections.Counter(content)	
	
	return [digest for digest in content_counter if content_counter[digest] > 1]

def avg_1_by_row(binary_content):
	count_1 = [float(binary_string.count('1')) / len(binary_string) for binary_string in binary_content]
	
	return sum(count_1) / len(count_1)

def avg_1_by_column(binary_content):
	col_sum_list = {}
	for x in range(0, 32):
		col_sum_list[x] = 0

	for binary_string in binary_content:
		blank_spaces = 32 - len(binary_string)
		binary_string = blank_spaces * '0' + binary_string

		for i in range(0, 32):
			if binary_string[i] is '1':
				col_sum_list[i] = col_sum_list[i] + 1

	return { k: float(v)/len(binary_content) for k, v in col_sum_list.items() }

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

def entropy(list):
	counter = collections.Counter(list)
	entropy = 0
	for key, value in counter.items():

		probability = value/float(len(list))
		entropy = entropy + (probability * math.log((1 / probability), 2))* value

	return entropy

def pairwise_xor(binary_content):
	y_axis = []
	x_axis = []
	z = {}

	for i in range(0, len(binary_content), 2):
		y_axis.append(xor(binary_content[i], binary_content[i+1]).count('1'))
		x_axis.append(i / 2)
		z[i / 2] = xor(binary_content[i], binary_content[i+1]).count('1')

	return x_axis, y_axis

check_for_arguments(sys.argv)

orig_file   = read_file(sys.argv[1])
orig_binary = hex_to_binary(orig_file)

alt_file    = read_file(sys.argv[2])
alt_binary  = hex_to_binary(alt_file)


print "The number of collisions in the .orig file are: {0}".format(len(collisions(orig_file)))
print "The number of collisions in the .alt file are: {0}".format(len(collisions(alt_file)))
print "The collisions in the .alt file are: {0}".format(collisions(orig_file))
print "Avg of row wise occurence of 1 and 0 are: {0} and {1}".format(avg_1_by_row(orig_binary), 1 - avg_1_by_row(orig_binary))

col_1_avg = avg_1_by_column(orig_binary)
print "Column wise avg occurrence of 1 is: {0}".format(col_1_avg)
print "Column wise avg occurrence of 1 for alt is: {0}".format(avg_1_by_column(alt_binary))

column_index = col_1_avg.keys()
y_pos        = np.arange(len(column_index))
y_values     = col_1_avg.values()

plt.bar(y_pos, y_values, align='center', alpha=0.5)
plt.xticks(y_pos, column_index)
plt.ylabel('Avg ocuurence of 1')
plt.xlabel('Column number')
plt.title('Average Occurence of 1 per column')
plt.show()

x_axis, y_axis = pairwise_xor(alt_binary)

plt.scatter(x_axis, y_axis)
plt.title('Difference in bits between orig and mod')
plt.ylabel('Number of bits changed')
plt.xlabel('File Number')
plt.show()

print "Entroy over digests in orig file: {0}".format(entropy(orig_file))
print "Entroy over digests in alt file: {0}".format(entropy(alt_file))
