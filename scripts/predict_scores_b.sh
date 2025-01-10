#!/bin/bash

## Predict variant scores using Basenji (https://github.com/calico/basenji)

## Author: Mondragon-Estrada E. et al.
## Last reviewed: April 2024
## Copyright (c) Mondragon-Estrada E. et al., 2024

help () {
         echo -e "\nPredict scores with Basenji"
         echo -e "Usage: predict_scores_b.sh [outdir] [.vcf]"
}

if [ $# -ne 2 ]
then
    help
    exit 1
else
    outdir=$1
    vcf=$2
fi

genome='data/hg38.fa'
targets='models/human_basenji/targets_human.txt'
architecture='models/params_human.json'
model='models/human_basenji/model_human_basenji.h5'

conda activate basenji

basenji_sad.py -f ${genome} \
-o ${outdir} \
--rc \
--shift "1,0,-1" \
-t ${targets} ${architecture} ${model} ${vcf}
