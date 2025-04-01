# BaNaNA - Barcoding Nanopore Neat Annotation

BaNaNA is a Snakemake pipeline designed to create high-quality OTUs (Operational Taxonomic Units) from Oxford Nanopore environmental amplicons. The pipeline was optimised for evaluation of general protist diversity based on 18S rDNA gene, however it is possible to choose different fragment of rDNA, including 16S rDNA. The main version of the pipeline was optimised for kit 14 Nanopore chemistry and R10.4 flow cell, however in the last part of a pipeline we describe approach for kit 9 chemistry. 


## Installation and setting up the pipeline

### 1. First make sure, that your conda those two channels added: `conda-forge` and `bioconda`:

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

### 3. Get the pipeline

### 4. Create a folder for samples

```
mkdir samples
```

### 5. Make the scripts exacutable

```
chmod a+x scripts/*
```


## Running the pipeline





































SNAKEMAKE


conda create -c conda-forge -c bioconda -n snakemake snakemake

snakemake --use-conda --conda-create-envs-only

scripts executable

chmod a+x *

snakemake --configfile config.yaml --use-conda

snakemake --dag | dot -Tpng > dag.png

snakemake --conda-cleanup-envs


conda config --show channels

channels:
  - conda-forge
  - bioconda
  - defaults

conda config --add channels <channel_name>
