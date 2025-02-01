#!/usr/bin/env python3

from argparse import ArgumentParser
from Bio import SeqIO



def parse_options():
	parser = ArgumentParser(description = 'remove sequences with big amont of N')
	parser.add_argument('-i', '--input', required = True, help = 'path to the input FASTA file')
	parser.add_argument('-o', '--output', required = True, help = 'name of the output FASTA file')
	return parser.parse_args()



def remove_Nseq(file):
	new_seq_file = []
	for seq in SeqIO.parse(file, 'fasta'):
		first_quarter = list(seq.seq)[:len(list(seq.seq))//4]
		forth_quarter = list(seq.seq)[3*len(list(seq.seq))//4:]
		n_counts1 = 0
		for letter in first_quarter:
			if letter == 'N' or letter =='n':
				n_counts1 += 1
		n_counts2 = 0
		for letter in forth_quarter:
			if letter == 'N' or letter =='n':
				n_counts2 += 1

		if n_counts1 < 20 and n_counts2 < 20:
			new_seq_file.append(seq)
	return new_seq_file




def save_final(final_seqs, out):
	with open(out, 'w') as output:
		SeqIO.write(final_seqs, output, 'fasta')




def main():
	options = parse_options()
	new_file = remove_Nseq(options.input)
	final = save_final(new_file, options.output)




if __name__ == '__main__':
	main()