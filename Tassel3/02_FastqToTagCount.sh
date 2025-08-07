#!/bin/bash
run_pipeline.pl -Xmx250g -Xms100g -fork1 -FastqToTagCountPlugin \
-i /home/share/GBS_honeybee/Run2/data/fastq/fastq \
-k /home/share/GBS_honeybee/Run2/data/key/Combined_keyfile.txt \
-o /home/share/GBS_honeybee/Run2/Tassel3_pipeline/ourdata/tagCounts \
-c 1 -e MspI-ApeKI -s 900000000 -endPlugin -runfork1

#Usage is as follows:
# -w  Working directory to contain subdirectories
# -e  Enzyme used to create the GBS library
# -s  Maximum number of good, barcoded reads per lane. Default: 200000000
##RB: For full flowcells set this to 400M as we see up to 33.3 Gbp, that's 333,000,000 reads
# -c  Minimum number of tags seen to output to file, Default: 1