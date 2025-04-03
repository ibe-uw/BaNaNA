# BaNaNA - Barcoding Nanopore Neat Annotator

BaNaNA is a Snakemake pipeline designed to create high-quality OTUs (Operational Taxonomic Units) from Oxford Nanopore environmental amplicons. The pipeline was optimised for evaluation of general protist diversity based on 18S rDNA gene, however it is possible to choose different rDNA gene, including 16S rDNA gene. The main version of the pipeline was optimised for Kit 14 Nanopore chemistry, however we separately describe an approach for Kit 9 chemistry. 

Scheme of the pipeline:

![Scheme of the pipeline](imgs/pipeline_scheme.png)


<!--- TOC START -->
Table of Contents
-----------------
- [Installation and setting up the pipeline](#installation-and-setting-up-the-pipeline)
- [Configurate BaNaNA](#configurate-banana)
- [Run BaNaNA](#run-banana)
- [Run BaNaNA for kit 9 chemistry](#run-banana-for-kit-9-chemistry)
- [Cite BaNaNA](#cite-banana)
<!--- TOC END -->


## Installation and setting up the pipeline

### 1. Check for conda channels

First, make sure that your conda has the `conda-forge` and the `bioconda` channels added

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

### 3. Download the repository

Download the repository to your prefered location using `git`:

```
git clone https://github.com/mchwalinska/BaNaNA.git
```

### 4. Create a folder in which all the analysis will be performed and make the python scripts exacutable

```
cd BaNaNA
mkdir samples
chmod a+x scripts/*
```


## Configurate BaNaNA

Adjust the run for your specific case by modifing options in the `config.yaml` file. ***The exemplary config file is located in the `suppl` folder.***

* `sample_name`: Provide names of you samples.

The names should not contain any special signs except `-` and `_`. Also they need to be the same as the names of the FASTQ files. For example, if your files are `BAB10.fastq` and `MIK3.fastq`, then the `sample_name` option should look like this:

```
sample_name:
 - BAB10
 - MIK3
```

* `threads`: Number of threads to use by softwares called in the pipeline. 
* `min_len_filtering`: Lover threshold for your amplicon length filtering. 
* `max_len_filtering`: Upper threshold for your amplicon length filtering. 
* `rrnas`: Your amplicons may be longer than 18S rDNA gene and contain multiple rDNA genes (like 5.8S rDNA and 28S rDNA for eukaryotes). Specify all rDNA genes included in your whole amplicon and their minimal length contained in the amplicon.

If your amplicon contains three genes, this option should look like this:

```
rrnas: 18S_rRNA:1000,5_8S_rRNA:90,28S_rRNA:400
```

And if you amplicon contains only 18S rDNA gene, this option should look like this:

```
rrnas: 18S_rRNA:1000
```

* `chosen_rrna`: Specify which rDNA gene, included in the `rrnas` option you want to keep for futher analysis. Choose only one gene, ***the default one is `18S_rRNA` gene***.
* `db_location`: Provide absolute path to the reference database you want to use to assign the taxonomy with.
* `db_id`: Specify minimal identity of OTUs to the closest reference sequence for taxonomic annotation. ***Default is `0.7`***.
* `db_query_cov`: Specify minimal coverage of OTUs to the closest reference sequence for taxonomic annotation. ***Default is `0.9`***.
* `enable_optional_taxonomy_format`: It's an optional step applied only for PR2 databse, which creates tab-separted table from raw VSEARCH output. If you are using different database than PR2, set this option to `false`.

Other options are optional to modify.


## Run BaNaNA

### 1. Copy your basecalled and demultiplexed FASTQ files to the folder `samples`

***The file configuration is important***. Your BaNaNA folder should look like this:

```
BaNaNA
├── Snakefile
├── config.yaml
├── envs
├── files
├── imgs
├── LICENSE
├── README.md
├── samples
|   ├── BAB10.fastq
|   └── MIK3.fastq
├── scripts
└── suppl
```

### 2. Activate snakemake conda environment

```
conda activate snakemake
```

### 3. Create necessary conda environments and install softwares

This is an optional step, as the environments would set up during the proper run, however we recoomend it, for the purpose to check if everything installed properly.

```
snakemake --use-conda --conda-create-envs-only
```

### 4. Run the analysis

This command will run the pipeline for all the samples provided in the `sample_name` option. The number of cores `-c` shouldn't be smaller than the `threads` number provided in the config file.

***Attention, the pipline takes long time to finish!*** 

```
snakemake –c 4 --configfile config.yaml --use-conda
```

## Run BaNaNA for kit 9 chemistry

The main pipeline is optimised for kit 14 chemisty. If you wish to run it for kit 9 chemistry, which characterises with lower quality, you need to replace the main `Snakefile` with the `Snakefile` from the `suppl` folder. The kit 9 version instead of clustering based on average error of the sample, performs the first clustering at 80% of identity.  


## Cite BaNaNA

If you are using our pipeline, please cite this paper






