#!/usr/bin/env python3

from argparse import ArgumentParser
from Bio import SeqIO




def parse_options():
	parser = ArgumentParser(description = '')
	parser.add_argument('-i', '--input', required = True, help = 'path to input input file')
	parser.add_argument('-sn', '--sample_name', required = True, help = 'sample name')
	parser.add_argument('-o', '--output', required = True, help = 'name of output file')
	return parser.parse_args()


def name_changer(file, sample):
	new_file = []
	for rec in SeqIO.parse(file, 'fasta'):
		rec.id = rec.id + '_' + sample
		new_file.append(rec)
	return new_file


def saving_output(final_file, output_file):
	with open(output_file, 'w') as output:
		SeqIO.write(final_file, output, 'fasta')



def main():
	options = parse_options()
	changed_file = name_changer(options.input, options.sample_name)
	saving = saving_output(changed_file, options.output)



if __name__ == '__main__':
	main()
