#!/bin/bash
tasselDir=/home/share/GBS_honeybee/tassel3-standalone/
${tasselDir}/run_pipeline.pl -Xmx250g -Xms100g -fork1 \
-UMergeTaxaTagCountPlugin -w . \
-t n -m 600000000 -x 100000000 -c 5 -endPlugin -runfork1

#Usage is as follows:
# -w  Working directory to contain subdirectories
# -t  Option to merge taxa (y/n). Default: y
##RB: We've decided to never merge taxa at this level. We run samples through without merging, check via KGD if merging is okay, then merge allelic counts.
# -m  Maximum tag number in the merged TagCount file. Default: 60000000
##RB: For full flowcells increase this from 60M to 600M
# -x  Maximum tag number in TagCount file for each taxa. Default: 10000000
##RB: For full flowcells increase this from 10M to 100M
# -c  Minimum count of a tag must be present to be output. Default: 5
##RB: As I understand it this is the overall count (all individuals) for a given tag
##    This value depends on the number of samples, MAF, sequence depth.
##    For 100 samples we have 2*100 = 200 alleles. We are interested in SNPs down to a MAF of 0.03. That would be 200*0.03 = 6.