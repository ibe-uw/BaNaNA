from argparse import ArgumentParser
from Bio import SeqIO


parser = ArgumentParser(description = 'nanopore statistics')
parser.add_argument('-i', '--input', required = True, help = 'path to input FASTA file')
parser.add_argument('-o', '--output', required = True, help = 'name of output file')
options = parser.parse_args()


# Save fasta file, key=header, value=record

recs_by_headers = {}

for seq in SeqIO.parse(options.input, 'fasta'):
	recs_by_headers[seq.id] = seq

# Save dictionary: { 'code_1': {'18s': ['header_1', 'header_2', ...], 
#							    '28s': [...], 
#							    '58s': [...]}, ...
#				    }

main_data = {}

for header, seq in recs_by_headers.items():
	code = seq.id.split(':')[2]

	if code not in main_data:
		main_data[code] = { '18s': [], '28s': [], '58s': [] }

	if header.startswith('18S_rRNA'):
		main_data[code]['18s'].append(header)
	elif header.startswith('28S_rRNA'):
		main_data[code]['28s'].append(header)
	elif header.startswith('5_8S_rRNA'):
		main_data[code]['58s'].append(header)

to_save_18 = []
one_copy_all = 0

all_18S = 0
red_18S = 0
one_18S = 0

all_58S = 0
red_58S = 0
one_58S = 0

all_28S = 0
red_28S = 0
one_28S = 0

for code, data in main_data.items():
	if len(data['18s']) == 1 and len(data['28s']) == 1 and len(data['58s']) == 1:
		for header in data['18s']:
			# here only headers we are interested in (18s + they have everything, 18, 28, 58s)
			to_save_18.append(recs_by_headers[header])
			one_copy_all += 1

	# make some statistics (can be deleted safely)
	if len(data['18s']) > 0:
		all_18S += 1
		if len(data['18s']) > 1:
			red_18S += 1
		if len(data['18s']) == 1:
			one_18S += 1


	if len(data['58s']) > 0:
		all_58S += 1
		if len(data['58s']) > 1:
			red_58S += 1
		if len(data['58s']) == 1:
			one_58S += 1



	if len(data['28s']) > 0:
		all_28S += 1
		if len(data['28s']) > 1:
			red_28S += 1
		if len(data['28s']) == 1:
			one_28S += 1


print(f"All 18S: {all_18S}")
print(f"Redundant 18s from them: {red_18S}")
print(f"18S with one copy: {one_18S}")


print(f"All 58S: {all_58S}")
print(f"Redundant 58s from them: {red_58S}")
print(f"18S with one copy: {one_58S}")


print(f"All 28S: {all_28S}")
print(f"Redundant 28s from them: {red_28S}")
print(f"18S with one copy: {one_28S}")


print(f"One copy of all fragments: {one_copy_all}")


with open(options.output, 'w') as output:
    SeqIO.write(to_save_18, output, 'fasta')




