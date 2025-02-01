#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path



def parse_options():
        parser = ArgumentParser(description = 'script to create otu table')
        parser.add_argument('-t', '--taxonomy', required = True, help = 'taxonomy file')
        parser.add_argument('-i', '--input_files', required = True, help = 'folder with abundance files')
        parser.add_argument('-o', '--output', required = True, help = 'name of output file')
        return parser.parse_args()



def import_otu_headers(tax_file):
        tax_header_list = []
        with open(tax_file) as tax:
                for line in tax.readlines():
                        new_l = [line.split('\t')[0].strip()]
                        tax_header_list.append(new_l)
        return tax_header_list



def data_frame(file, tax):
        header_list = []
        whole_list = []
        with open(file) as i:
                for l in i.readlines():
                        whole_list.append(l.strip().split('\t'))
                        header_list.append(l.strip().split('\t')[0])
        for t in tax:
                if t[0] in header_list:
                        for l in whole_list:
                                if t[0] == l[0]:
                                        t.append(l[1])
                else:
                        t.append(str(0))
        return tax



def saving_output(headers, data_fr, output_file):
        final_file_body = ''
        with open (output_file, 'w') as output:
                header = 'OTU' + '\t' + '\t'.join(headers) + '\n'
                for rec in data_fr:
                        new_line = "\t".join(rec) + '\n'
                        final_file_body = final_file_body + new_line
                output.write(header + final_file_body)




def main():
        options = parse_options()
        taxonomy_headers = import_otu_headers(options.taxonomy)

        files = Path(options.input_files).glob('abundance_*')
        header_l = []
        for file in files:
                df = data_frame(file, taxonomy_headers)
                header_l.append('_'.join(str(file).split("_")[1:5]).split('.')[0])


        saving = saving_output(header_l, df, options.output)




if __name__ == '__main__':
        main()