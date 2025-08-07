#!/bin/bash
tasselDir=/home/share/GBS_honeybee/tassel3-standalone/
${tasselDir}/run_pipeline.pl -Xmx250g -Xms100g -fork1 \
-UTBTToMapInfoPlugin -w . -endPlugin -runfork1

#Usage is as follows:
# -w  Working directory to contain subdirectories