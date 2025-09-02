#!/bin/bash

REFERENCE= # Location of the reference genome
CONDA_ENV= # Conda environment where dependencies are installed
ADAPTER= # Adapter sequence

# Restriction enzyme names
ENZYME_1=
ENZYME_2=

# Sequential numbers of the columns in ./metadata/keyfile.tsv that contain the respective information
LIBRARYPREPID_COLUMN= 
BARCODE_COLUMN=
FLOWCELL_COLUMN=
LANE_COLUMN=
SAMPLE_COLUMN=