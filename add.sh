#!/bin/sh

args=("$@")
if [ $# -eq 0 ]; then
    echo "Usage: ./add.sh <file>"
    exit 1
fi

file_path=${args[0]}

ipfs_cmd= ($(ipfs add -r $file_path --progress=false > ipfs_pins.tsv)) 

counter=1
lines_per_file=50000
total_lines=$(wc -l < ipfs_pins.tsv)

while [ $counter -le $total_lines ]; do
    start_line=$counter
    end_line=$((counter + lines_per_file - 1))
    split_file="split-$counter-to-$end_line.tsv"
    sed -n "${start_line},${end_line}p;${end_line}q" ipfs_pins.tsv > $split_file
    counter=$((counter + lines_per_file))
done

mkdir ipfs_pins
mv split-*.tsv ipfs_pins
node convert.js ipfs_pins
rm ipfs_pins.tsv