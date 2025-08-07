#!/bin/bash
tasselDir=/home/share/GBS_honeybee/tassel3-standalone/
${tasselDir}/run_pipeline.pl -fork1 -UCreatWorkingDirPlugin -w . -endPlugin -runfork1

#Usage is as follows:
# -w  Working directory to contain subdirectories