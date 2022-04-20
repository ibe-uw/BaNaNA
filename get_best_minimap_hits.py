#!/usr/bin/env python3
from argparse import ArgumentParser
from pprint import pprint

def parse_arguments():
	parser = ArgumentParser(description = 'Get the best hits from PAF file for each sequence')
	parser.add_argument('-i', '--input', required = True, help = 'path to input PAF file')
	parser.add_argument('-o', '--output', required = True, help = 'name of output file')
	return parser.parse_args()


def main():
	arguments = parse_arguments()

	# Preparing the data to work with

	# { 'c106e85d-395a-42d1-95cc-5e5928d3a771': [
	#					{
	#					   'org_name': 'DQ244038.1.1775_U|Eukaryota|Al...', 
	#					   'match_cnt': 4,
	#					   'quality': '42'
	#					}, ...], ... }
	hits_by_seq_codes = {}

	with open(arguments.input) as f:
		for line in f:
			line = line.strip()
			if line == '':
				continue

			splitted = line.split('\t')

			seq_code = splitted[0].split(':')[2]

			if seq_code not in hits_by_seq_codes:
				hits_by_seq_codes[seq_code] = []

			hit_obj = {}
			hit_obj['org_name'] = splitted[5]
			hit_obj['match_cnt'] = int(splitted[9])
			hit_obj['quality'] = int(splitted[11])

			hits_by_seq_codes[seq_code].append(hit_obj)


	# Fetching the best hit for each sequence

	# { 'c106e85d-395a-42d1-95cc-5e5928d3a771': {
	#					   'org_name': 'DQ244038.1.1775_U|Eukaryota|Al...', 
	#					   'match_cnt': 4,
	#					   'quality': '42'
	#					}, ... }
	best_hits_by_seq_codes = {}

	for seq_code, hits in hits_by_seq_codes.items():

		hits.sort(key=lambda e: (-e['quality'], e['match_cnt']))
		best_hit = hits[-1]

		best_hits_by_seq_codes[seq_code] = best_hit


	# Saving the results
	# 😂
	#  🍆

	with open(arguments.output, 'w') as out_f:
		for seq_code, hit in best_hits_by_seq_codes.items():

			line = '\t'.join([seq_code, hit['org_name']]) + '\n'
			out_f.write(line)



main()
