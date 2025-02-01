#!/usr/bin/env python3

from argparse import ArgumentParser
from Bio import SeqIO
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import glob
import os
from joblib import Parallel, delayed
from pathlib import Path




GAP_TRESHOLD = 0.5
CONSENSUS_TRESHOLD = 0.5 
LETTERS = ('A', 'T', 'G', 'C', '-')



def parse_options():
	parser = ArgumentParser(description = 'performs cluster size filtering, alignment and creates consesus')
	parser.add_argument('-i', '--input', required = True, help = 'name of the folder with clusters')
	parser.add_argument('-a', '--alignment', required = True, help = 'path to the file with alignments')
	parser.add_argument('-t', '--threads', required = True, help = '')
	parser.add_argument('-o', '--output', required = True, help = 'output file name')
	return parser.parse_args()



def filtering(folder):
	for cluster in glob.glob(f'{folder}/cluster*'):
		clust = list(SeqIO.parse(cluster,'fasta'))
		if len(clust) < 4:
			os.remove(cluster)



def mafft(aln_folder, cluster):
	os.system(f'mafft {cluster} > {aln_folder}{cluster.split("/")[2]}')



def count_for_position(string):
	counts = {}
	for letter in LETTERS:
		counts[letter] = string.count(letter)
	return counts



def classic_consensus(counts):
	total = sum(counts.values())
	if counts['-']/total > GAP_TRESHOLD:
		return('')
	else:
		if counts[(max(counts, key=counts.get))]/total > CONSENSUS_TRESHOLD:
			return((max(counts, key=counts.get)))
		else:
			return('N')



def save_file(to_write, out):
	with open(out, 'w') as output: 
		SeqIO.write(to_write, output, 'fasta')





def main():
	options = parse_options()
	filtering_folders = filtering(options.input)
	filt_clusters = glob.glob(f'{options.input}/cluster*')
	result = Parallel(n_jobs=options.threads, prefer='threads')(delayed(mafft)(options.alignment, i) for i in filt_clusters)

	seqs_to_write = []
	for aln_cluster in glob.glob(f'{options.alignment}/*'):
		consensus = ''
		alignments = AlignIO.read(aln_cluster, 'fasta') 
		for position in range(alignments.get_alignment_length()-1):
			position_line = (alignments[:, position].upper())
			counts_results = count_for_position(position_line)
			consensus = consensus + classic_consensus(counts_results)
		seq = Seq(consensus)
		id_header = aln_cluster.split('/')[3]
		record = SeqRecord(seq,id=id_header, description= '')
		seqs_to_write.append(record)
	final = save_file(seqs_to_write, options.output)




if __name__ == '__main__':
	main()