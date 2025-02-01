#!/usr/bin/env python3

from argparse import ArgumentParser

def parse_options():
	parser = ArgumentParser(description = 'extracts mean quality value and calculates clustering treshold value')
	parser.add_argument('-s', '--stats', required = True, help = 'path to the NanoStats.txt, output of NanoPlot')
	parser.add_argument('-e', '--error_table', required = True, help = 'path to the P_error_table.tsv file')
	parser.add_argument('-o', '--output_file', required = True, help = '')
	return parser.parse_args()


def formating_files(file):
	input_list = []
	with open(file) as input_file:
		for line in input_file.readlines():
			input_list.append(line.strip())
	input_dict = {}
	for values in input_list:
		input_dict[values.split('\t')[0]] = values.split('\t')[1]

	return input_dict


def treshold_calculations(stats_dict, erro_dict):
	quality = int(round(float(stats_dict['mean_qual']), 0))
	p_error = float(erro_dict[str(quality)])
	seq_quality = round(1 - p_error, 3)
	return seq_quality 


def save_final(final_out, out):
	with open(out, 'w') as output:
		output.write(f'{final_out}\n')



def main():
	options = parse_options()
	stats_d = formating_files(options.stats)
	error_d = formating_files(options.error_table)
	clustering_treshold = treshold_calculations(stats_d, error_d)
	output_file = save_final(clustering_treshold, options.output_file)


if __name__ == '__main__':
	main()


