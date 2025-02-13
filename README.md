SNAKEMAKE
conda create -c conda-forge -c bioconda -n snakemake snakemake
snakemake --use-conda --conda-create-envs-only
scripts executable
chmod a+x *
snakemake --configfile config.yaml --use-conda
snakemake --dag | dot -Tpng > dag.png


snakemake --conda-cleanup-envs
