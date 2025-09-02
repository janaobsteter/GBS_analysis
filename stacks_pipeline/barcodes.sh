#!/bin/bash

# Source config variables
source config.sh

# For each library in the input/metadata/keyfile.tsv
libraryprepids=$(cut "-f${LIBRARYPREPID_COLUMN}" ./metadata/keyfile.tsv | sed '/libraryprepid/d' | sort | uniq)
for libraryprepid in $libraryprepids; do
    # Extract all barcodes used in that library and write them to input/metadata/barcodes_<library-prep-id>.txt
    awk -v libraryprepid="$libraryprepid" \
        "\$${LIBRARYPREPID_COLUMN}==libraryprepid {print \$${BARCODE_COLUMN}}" \
        './metadata/keyfile.tsv' \
        | sort | uniq \
        > "./metadata/barcodes_${libraryprepid}.txt"
done