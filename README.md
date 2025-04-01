# BaNaNA - Barcoding Nanopore Neat Annotation

BaNaNA is a Snakemake pipeline designed to create high-quality OTUs (Operational Taxonomic Units) from Oxford Nanopore environmental amplicons. The pipeline was optimised for evaluation of general protist diversity based on 18S rDNA gene, however it is possible to choose different fragment of rDNA, including 16S rDNA. The main version of the pipeline was optimised for kit 14 Nanopore chemistry and R10.4 flow cell, however in the last part of a pipeline we describe approach for kit 9 chemistry. 


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

To adjust the analysis for your specific case modify further oprions in the `config.yaml` file:

* `sample_name`:
* `threads`:
* `min_len_filtering`:
* `max_len_filtering`:
* `rrnas`:
* `chosen_rrna`:
* `db_location`: Provide absolute path to the reference database you want to use to assign the taxonomy.
* `db_id`: Minimal threashold for identity to 
* `db_query_cov`:
* `enable_optional_taxonomy_format`:

Other options are optional to modify.


## Run BaNaNA


## Cite BaNaNA

If you are using our pipeline, please cite this paper






