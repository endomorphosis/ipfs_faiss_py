#!/bin/sh

# 1 million line split using split command

counter=1
lines_per_file=50000
total_lines=$(wc -l < Caselaw_Access_Project_JSON_pins.tsv)

while [ $counter -le $total_lines ]; do
    start_line=$counter
    end_line=$((counter + lines_per_file - 1))
    split_file="split-$counter-to-$end_line.tsv"
    sed -n "${start_line},${end_line}p;${end_line}q" Caselaw_Access_Project_JSON_pins.tsv > $split_file
    counter=$((counter + lines_per_file))
done
mkdir ipfs_pins
mv split-*.tsv ipfs_pins
node convert.js ipfs_pins
rm Caselaw_Access_Project_JSON_pins.tsv