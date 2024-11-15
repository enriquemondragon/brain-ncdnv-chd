#!/usr/bin/env python3

'''
Filters scores from an indexed list of epigenome marks by Enrique Mondragon Estrada 2022
'''

def filter_scores(score_file, filter_file, out_path):
    
    import pandas as pd

    sad_df = pd.read_csv(score_file, delimiter='\t')
    sad_df = sad_df.drop(['chrom', 'pos', 'ID', 'ref', 'alt'], axis=1)
    filter_df = pd.read_csv(filter_file)

    print(sad_df)
    print(filter_df)

    idx = filter_df['index']
    print(idx)

    sad_filter_df = sad_df.iloc[: , idx].copy()
    print(sad_filter_df)

    path = out_path + 'sad_scores_fltr.csv'
    sad_filter_df.to_csv (path, index = False, header=True, sep ='\t')
    print('saved!')

import argparse

parser = argparse.ArgumentParser(description=' ========== Filter scores from an indexed list of epigenome marks by Enrique Mondragon Estrada 2022 ==========', usage='%(prog)s')
parser.add_argument('-score', '--score_file', type=str, required=True, help='sad file', dest='score_file')
parser.add_argument('-filter', '--filter_file', type=str, required=True, help='filter file', dest='filter_file')
parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')

args = parser.parse_args()
score_file = args.score_file
filter_file = args.filter_file
out_path = args.out_path

filter_scores(score_file, filter_file, out_path)