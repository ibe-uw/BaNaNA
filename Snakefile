configfile: "config.yaml"


rule all:
	input:
		expand("samples/abundance_{sample}.tsv", sample=config["sample_name"]),
		"samples/taxonomy.tsv",
		expand("samples/taxonomy.tsv", allow_missing=True) if config["enable_optional_taxonomy_format"] else [],
		"samples/otu_table.tsv"
		





rule filtlong:
	input: 
		"samples/{sample}.fastq"
	output: 
		"samples/filtlong_{sample}.fastq"
	conda:
		"envs/filtlong.yaml"
	params:
		min_len = config["min_len_filtering"],
		max_len = config["max_len_filtering"],
		min_q = config["min_mean_quality_filering"]
	shell:
		"filtlong --min_length {params.min_len} --max_length {params.max_len}  --min_mean_q {params.min_q} {input} > {output}"


rule sed:
	input:
		"samples/filtlong_{sample}.fastq"
	output:
		"samples/filtlong_{sample}.fasta"
	shell:
		"sed -n '1~4s/^@/>/p;2~4p' {input} > {output}"


rule barrnap:
	input:
		"samples/filtlong_{sample}.fasta"
	output:
		"samples/barrnap_{sample}.fasta"
	conda:
		"envs/barrnap.yaml"
	threads: config["threads"]
	shell:
		"barrnap --kingdom euk --reject 0.1 --outseq {output} {input} --threads {threads}"


rule extract_rrna:
	input:
		"samples/barrnap_{sample}.fasta"
	output:
		"samples/rrna_extracted_{sample}.fasta"
	conda:
		"envs/python.yaml"
	params:
		rrna = config["rrnas"],
		chosen = config["chosen_rrna"]
	log:
		"samples/rrna_extraction_stats_{sample}.txt"
	shell:
		"scripts/extracting_rrna.py -i {input} -r {params.rrna} -cr {params.chosen} -o {output} > {log}"


rule nanoplot:
	input:
		"samples/filtlong_{sample}.fastq"
	output:
		directory("samples/nanoplot_{sample}")
	conda:
		"envs/nanoplot.yaml"
	threads: config["threads"]
	shell:
		"NanoPlot --fastq {input} --tsv_stats -t {threads} --info_in_report -o {output}"


rule clust_threshold:
	input:
		"samples/nanoplot_{sample}"
	output:
		"samples/clust_file_{sample}.txt"
	conda:
		"envs/python.yaml"
	shell:
		"scripts/calculate_clustering_threshold.py -s {input}/NanoStats.txt -e files/P_error_table.tsv -o {output}"


rule error_clustering:
	input:
		fa = "samples/rrna_extracted_{sample}.fasta",
		idt = "samples/clust_file_{sample}.txt"
	output:
		directory("samples/clusters_error_{sample}/")
	threads: config["threads"]
	conda:
		"envs/python.yaml"
	shell:
		"mkdir -p {output} && vsearch --cluster_fast {input.fa} -id $(cat {input.idt}) --threads {threads} --clusters {output}/cluster"


rule consensus:
	input:
		"samples/clusters_error_{sample}/"
	output:
		"samples/consensus_{sample}.fasta"
	conda:
		"envs/python.yaml"
	threads: config["threads"]
	shell:
		"mkdir -p {input}/alignments && scripts/mafft_consensus.py -i {input} -a {input}/alignments/ -t {threads} -o {output}"


rule minimap:
	input:
		ce = "samples/clusters_error_{sample}/",
		fai = "samples/consensus_{sample}.fasta"
	output:
		mo = directory("samples/minimap_out_{sample}/"),
		paf = "samples/minimap_out_all_{sample}.paf"
	conda:
		"envs/python.yaml"
	threads: config["threads"]
	shell:
		"mkdir -p {output.mo} && scripts/minimap.py -c {input.fai} -cl {input.ce} -t {threads} -o {output.mo} && cat {output.mo}/* > {output.paf}"


rule racon:
	input:
		fai = "samples/rrna_extracted_{sample}.fasta",
		paf = "samples/minimap_out_all_{sample}.paf",
		con = "samples/consensus_{sample}.fasta"
	output:
		"samples/racon_{sample}.fasta"
	conda:
		"envs/racon.yaml"
	params: config["min_mean_quality_polishing"]
	threads: config["threads"]
	shell:
		"racon {input.fai} -q {params} -w 500 -t {threads} {input.paf} {input.con} > {output}"


rule add_names:
	input:
		"samples/racon_{sample}.fasta"
	output:
		"samples/racon_name_{sample}.fasta",
	conda:
		"envs/python.yaml"
	shell:
		"scripts/add_sample_id.py -i {input} -sn {wildcards.sample} -o {output}"


rule merging:
	input:
		expand("samples/racon_name_{sample}.fasta", sample=config["sample_name"])
	output:
		"samples/merged.fasta"
	shell:
		"cat {input} > {output}"


rule chimeras:
	input:
		"samples/merged.fasta"
	output:
		fao1 = "samples/nonchim_db.fasta",
		fao2 = "samples/nonchim_db_dn.fasta"
	conda:
		"envs/python.yaml"
	threads: config["threads"]
	params: 
		db = config["db_location"]
	shell:
		"vsearch --uchime_ref {input} --db {params.db} --threads {threads} --nonchimeras {output.fao1} && vsearch --uchime2_denovo {output.fao1} --threads {threads} --nonchimeras {output.fao2}"


rule final_clustering:
	input:
		"samples/nonchim_db_dn.fasta"
	output:
		"samples/pre_otus.fasta"
	conda:
		"envs/python.yaml"
	threads: config["threads"]
	shell:
		"mkdir -p samples/clusters_final/ && vsearch --cluster_fast {input} -id 0.99 --threads {threads} --clusters samples/clusters_final/cluster --centroids {output}"


rule remove_N_seqs:
	input:
		"samples/pre_otus.fasta"
	output:
		"samples/otus.fasta"
	conda:
		"envs/python.yaml"
	shell:
		"scripts/remove_Nseqs.py -i {input} -o {output}"


rule taxonomy:
	input:
		"samples/otus.fasta"
	output:
		tax1 = "samples/taxonomy.tsv",
		tax2 = "samples/taxonomy_table.tsv"
	conda:
		"envs/python.yaml"
	threads: config["threads"]
	params:
		db = config["db_location"],
		ident = config["db_id"],
		cov = config["db_query_cov"]
	shell:
		"vsearch --usearch_global {input} --db {params.db} --id {params.ident} --threads {threads} --blast6out {output.tax1}  --query_cov {params.cov} && scripts/get_taxonomy_table.py -i {output.tax1} -o {output.tax2}"


rule abundance:
	input:
		fai = "samples/otus.fasta",
		ce = "samples/clusters_error_{sample}/"
	output:
		ab = "samples/abundance_{sample}.tsv"
	conda:
		"envs/python.yaml"
	shell:
		"scripts/abundance.py -otu {input.fai} -fclu samples/clusters_final/ -eclu {input.ce} -sn {wildcards.sample} -o {output.ab}" 


rule otu_table:
	input:
		"samples/taxonomy.tsv"
	output:
		"samples/otu_table.tsv"
	conda:
		"envs/python.yaml"
	shell:
		"scripts/get_otu_table.py -t {input} -i ./samples/ -o {output}"

