#!/usr/bin/env python3

from Bio import SeqIO
from argparse import ArgumentParser


def parse_options():
	parser = ArgumentParser(description = 'rRNA filtering and fragment extraction')
	parser.add_argument('-i', '--input', required = True, help = 'path to input FASTA file')
	parser.add_argument('-r', '--rrnas', required = True, help = '')
	parser.add_argument('-cr', '--chosen_rrna', required = True, help = '')
	parser.add_argument('-o', '--output', required = True, help = 'name of output file')
	return parser.parse_args()



def rrna_dictionary(rrna):
	rna_dict = {item.split(':')[0]: int(item.split(':')[1]) for item in rrna.split(',')}
	return rna_dict



def create_data_dict(file, rrnas):
	main_data = {}
	for record in SeqIO.parse(file, 'fasta'):
		rna_type, code = record.id.split(':')[0], record.id.split(':')[2]
		if rna_type not in rrnas.keys():
			continue
		if code not in main_data:
			main_data[code] = {rna: [] for rna in rrnas}
		if len(record.seq) > rrnas[rna_type]:
			main_data[code][rna_type].append(record)
	return main_data



def save_final(final_dict, chosen_rrna, out):
	to_save = []
	for code, data in final_dict.items():
		if all(len(data_list) == 1 for rna, data_list in data.items()):
			to_save.append(data[chosen_rrna])	

	with open(out, 'w') as output:
		for record in to_save:
			SeqIO.write(record, output, 'fasta')



def statistics(final_dickt, rrna):
	all_codes = 0
	one_detection = 0
	multiple_detection = 0
	no_detection = 0
	for code, dickt in final_dickt.items():
		all_codes += 1
		if len(dickt[rrna]) == 1:
			one_detection += 1
		if len(dickt[rrna]) > 1:
			multiple_detection += 1
		if len(dickt[rrna]) == 0:
			no_detection += 1

	print(f"All sequences: {all_codes}")
	print(f"{rrna} detected once: {one_detection}")
	print(f"{rrna} detected multiple times: {multiple_detection}")
	print(f"{rrna} not detected: {no_detection}")




def main():
	options = parse_options()
	rrna_dict = rrna_dictionary(options.rrnas)
	main_rrna_dickt = create_data_dict(options.input, rrna_dict)
	final = save_final(main_rrna_dickt, options.chosen_rrna, options.output)

	for rna, lenght in rrna_dict.items():
		statistics(main_rrna_dickt, rna)



if __name__ == '__main__':
	main()















