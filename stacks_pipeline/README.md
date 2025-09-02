# Configuration

- Copy or symlink fastq files to be processed into fastq/
- Rename files in fastq/ according to the format SQ<libraryprepid>_<flowcell>_s_<lane>.fq.gz
- Copy or symlink reference genome into reference/
- Copy or symlink keyfile to metadata/keyfile.tsv
- Set variables in config.sh
- Generate barcode files with ./barcodes.sh
- Adjust slurm parameters, thread settings in scripts
- Index reference genome with ./index.slurm