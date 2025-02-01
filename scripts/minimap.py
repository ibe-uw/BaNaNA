#!/usr/bin/env python3

import glob
from Bio import SeqIO
import os
from argparse import ArgumentParser
from pathlib import Path



def parse_options():
	parser = ArgumentParser(description = '')
	parser.add_argument('-c', '--consensus', required = True, help = '')
	parser.add_argument('-cl', '--cluster_folder', required = True, help = '')
	parser.add_argument('-o', '--output', required = True, help = '')
	parser.add_argument('-t', '--threads', required = True, help = '')
	return parser.parse_args()



def file_prep(file):
	cons_list = []
	for seq in SeqIO.parse(file, 'fasta'):
		cons_list.append(seq)
	return cons_list



def minimap(clusters, consensus, thread_num, output):
	for cluster in glob.glob(f'{clusters}/cluster*'):
		for cons in consensus:
			if str(cluster).split('/')[2] == cons.id:
				SeqIO.write(cons, f'{cons.id}.fasta', 'fasta')
				os.system(f"minimap2 {cons.id}.fasta {cluster} -t {thread_num} > {output}/minimap_{cons.id}.paf")
				os.remove(f'{cons.id}.fasta')




def main():
	options = parse_options()
	consensus_list = file_prep(options.consensus)
	mapping = minimap(options.cluster_folder, consensus_list, options.threads, options.output)




if __name__ == '__main__':
	main()