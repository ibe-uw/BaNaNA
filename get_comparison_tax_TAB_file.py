#!/usr/bin/env python3

from argparse import ArgumentParser
from pprint import pprint


def parse_arguments():
	parser = ArgumentParser(description = 'Get comparison of TAB taxonomic annotation files - blast minimap2')
	parser.add_argument('-b', '--blast_input', required = True, help = 'path to input blast TAB file')
	parser.add_argument('-m', '--minimap_input', required = True, help = 'path to input minimap2 best hit TAB file')
	parser.add_argument('-o', '--output', required = True, help = 'output identifier')
	return parser.parse_args()


def main():
	arguments = parse_arguments()



	

	def open_and_split(input):

		splitted = []
		with open(input) as i:

			for line in i:

				line = line.strip()

				splitted.append(line.split('\t'))

		return splitted




	splitted_b = open_and_split(arguments.blast_input)

	splitted_m = open_and_split(arguments.minimap_input)




# Creating dictionary of annotation: {'a53af686-2726-4670-b498-898ff630d73a':
#														{'minimap': ['HQ219336.1.1722_U', 'Eukaryota', 'Alveolata'], 
#														 'blast': []}}


	combined_dict = {}
	
	for record in splitted_m:

		seq_code = record[0]

		mm_ann = {'minimap': record[1].split('|')}

		combined_dict[seq_code] = mm_ann


	
	

	for record2 in splitted_b:

		seq_code2 = record2[0].split(':')[2]

		for seq_code, ann in combined_dict.items():

			if seq_code2 == seq_code:

				ann['blast'] = record2[1].split('|')



			
		if seq_code2 not in combined_dict.keys():

			seq_code2_key = {'blast': record2[1].split('|')}

			combined_dict[seq_code2] = seq_code2_key

	


# Comparison of reference ids:

	all_ids = 0
	same_ids = 0
	not_two = 0
	not_two_list = []

	for seq_code, ann in combined_dict.items():


		all_ids = all_ids + 1


		if len(ann) != 2:

			not_two = not_two + 1 

			small_list = [seq_code, ann.keys(), ann.values()]

			not_two_list.append(small_list)




		elif len(ann) == 2:


			if ann['blast'][0] == ann['minimap'][0]:

				same_ids = same_ids + 1

	
	print(f'Number of sequences which don\'t have two annotations: {not_two}')
	print(f'Number of all annotated sequences: {all_ids}')
	print(f'Number of sequences with the same reference id from blast and minimap2: {same_ids}')




	with open(f'{arguments.output}_blast_minimap2_not_two_ann.tsv', 'w') as out1:

		for i in  not_two_list:

			out1.write(i[0] + '\t' + str(i[1]) + '\t' + str(i[2]) + '\n')




# Comparison of taxonomic levels:

	supergroup = 0
	division = 0
	tax_class = 0
	order = 0
	family = 0
	genus = 0

	for seq_code, ann in combined_dict.items():

		if len(ann) == 2:

			if ann['blast'][2] == ann['minimap'][2]:

				supergroup = supergroup + 1


			if ann['blast'][3] == ann['minimap'][3]:

				division = division + 1


			if ann['blast'][4] == ann['minimap'][4]:

				tax_class = tax_class + 1

			if ann['blast'][5] == ann['minimap'][5]:

				order = order + 1

			if ann['blast'][6] == ann['minimap'][6]:

				family = family + 1

			if ann['blast'][7] == ann['minimap'][7]:

				genus = genus + 1




	print(f'Number of sequences with the same supergroup annotation: {supergroup}')

	print(f'Number of sequences with the same division annotation: {division}')

	print(f'Number of sequences with the same tax_class annotation: {tax_class}')

	print(f'Number of sequences with the same order annotation: {order}')

	print(f'Number of sequences with the same family annotation: {family}')

	print(f'Number of sequences with the same genus annotation: {genus}')



# Getting taxonomy from files for plots:

	
	def save_tax(ann_key, separator):

		with open(f'{arguments.output}_{ann_key}_taxonomy.tsv', 'w') as out2:

			for seq_code, ann in combined_dict.items():

				if ann_key in ann.keys():

					out2.write(separator.join(ann[ann_key]) + '\n')


		return out2







	save_tax('minimap', '\t')

	save_tax('blast', '\t')







if __name__ == '__main__':
	main()