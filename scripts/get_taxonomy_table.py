#!/usr/bin/env python3

from argparse import ArgumentParser

def parse_options():
	parser = ArgumentParser(description = 'modify taxonomy file')
	parser.add_argument('-i', '--input', required = True, help = 'path to vsearch input file')
	parser.add_argument('-o', '--output', required = True, help = 'name of output file')
	return parser.parse_args()


def importing(file):
	input_list = []
	with open(file) as vsearch:
		for line in vsearch.readlines():
			input_list.append(line.split('\t'))
	return input_list


def create_dict(imported_list):
	file_dict = []
	for rec in imported_list:
		rec_dict = {'qseqid': rec[0], 'seqacc': rec[1].split(';')[0], 'seqtax': rec[1].split(';')[1], 'pident': rec[2], 'length': rec[3]}
		file_dict.append(rec_dict)
	return file_dict


def modify_seqtax(data):
    for entry in data:
        seqtax = entry['seqtax'].replace('tax=', '')
        parts = [part.split(':')[1] for part in seqtax.split(',')]
        entry['seqtax'] = '\t'.join(parts)
    return data


def saving_output(modif, output_file):
	final_file = ''
	with open(output_file, 'w') as output:
		header = 'OTU' + '\t' + 'Pident' + '\t' + 'Accession' + '\t' + 'Domain' + '\t' + 'Supergroup' + '\t' + 'Division' + '\t' + 'Subdivision' + '\t' + 'Class' + '\t' + 'Order' + '\t' + 'Family' + '\t' + 'Genus' + '\t' + 'Species' + '\t' + 'Length' + '\n'
		for l in modif:
			out_line = l['qseqid'] + '\t' + l['pident'] + '\t' + l['seqacc'] + '\t' + l['seqtax'].replace('-','\t') + '\t' + l['length'] + '\n'
			final_file = final_file + out_line
		output.write(header + final_file)


def main():
	options = parse_options()
	imported_file = importing(options.input)
	dictionary_file = create_dict(imported_file)
	modified_data = modify_seqtax(dictionary_file)
	saving = saving_output(modified_data, options.output)



if __name__ == '__main__':
	main()
