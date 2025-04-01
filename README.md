# BaNaNA - Barcoding Nanopore Neat Annotation

BaNaNA is a Snakemake pipeline designed to create high-quality OTUs (Operational Taxonomic Units) from Oxford Nanopore environmental amplicons. The pipeline was optimised for evaluation of general protist diversity based on 18S rDNA gene, however it is possible to choose different fragment of rDNA, including 16S rDNA. The main version of the pipeline was optimised for kit 14 Nanopore chemistry and R10.4 flow cell, however in the last part of a pipeline we describe approach for kit 9 chemistry. 

Scheme of the pipeline:

![Scheme of the pipeline](imgs/pipeline_scheme.png)


## Installation and setting up the pipeline

### 1. Check for conda channels

First, make sure that your conda the `conda-forge` and `bioconda`channels added

```
conda config --show channels
```

If they are missing add them with following commands:

```
conda config --add channels conda-forge
conda config --add channels bioconda
```

### 2. Install Snakemake in a separate conda environment

```
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

### 3. Get BaNaNA

```

```

### 4. Create a folder in which all the analysis will be performed and make the python scripts exacutable

```
mkdir samples
chmod a+x scripts/*
```


## Configurate BaNaNA

Adjust the analysis for your specific case modify further oprions in the `config.yaml` file. ***The exemplary config file is located in the folder `test_data`.***

* `sample_name`: Provide names of you samples. The names should not contain any special signs except `-` and `_`. Also they need to be the same as the names of the FASTQ files. For example, if your files are `BAB10.fastq` and MIK3.fastq`, then the `sample_name` option should look like this:

```
sample_name:
 - BAB10
 - MIK3
```

* `threads`: Number of threads to use by softwares called in the pipeline. 
* `min_len_filtering`: Lover threshold for your amplicon length filtering. 
* `max_len_filtering`: Upper threshold for your amplicon length filtering. 
* `rrnas`: Your amplicons may be longer than 18S rDNA gene and contain different rDNA genes (like 5.8S rDNA and 28S rDNA for eukaryotes). Specify all rDNA genes included in your whole amplicon and the minimal length of each gene.

If your amplicon contains three genes, this option should look like this:

```
rrnas: 18S_rRNA:1000,5_8S_rRNA:90,28S_rRNA:400
```

And if you amplicon contains only 18S rDNA gene, this option should look like this:

```
rrnas: 18S_rRNA:1000
```

* `chosen_rrna`: Specify which rDNA gene, included in the `rrnas` option you want to keep for futher analysis. Choose only one gene, ***the default one is 18S rDNA gene***.
* `db_location`: Provide absolute path to the reference database you want to use to assign the taxonomy.
* `db_id`: Specify minimal identity of OTUs to closest reference sequence for taxonomic annotation.
* `db_query_cov`: Specify minimal coverage of OTUs to closest reference sequence for taxonomic annotation.
* `enable_optional_taxonomy_format`: It's an optional step for PR2 databse, which creates tab-separted table from raw output of taxonomic annotation. If you are using different database, set this option to `false`.

Other options are optional to modify.


## Run BaNaNA




## Cite BaNaNA

If you are using our pipeline, please cite this paper






