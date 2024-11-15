#!/usr/bin/env python3

'''
Transforms Basenji2's scores from H5 to CSV format by Enrique Mondragon Estrada 2022
'''

def process_scores(sad_file):

        import h5py
        import re
        import pandas as pd

        sad_h5 = h5py.File(sad_file, 'r')

        scores = sad_h5['SAD']
        snps = sad_h5['snp']
        chr = sad_h5['chr']
        pos = sad_h5['pos']
        ref = sad_h5['ref_allele']
        alt = sad_h5['alt_allele']

        targets = sad_h5['target_labels']

        print('total of SNPs: ', scores.shape[0])
        print('total of targets: ', scores.shape[1])

        data = {'chr': chr, 
                'pos': pos, 
                'ID_SNP': snps,
                'ref': ref, 
                'alt': alt 
                }
        for target in range(targets.shape[0]):
                print(target)

        prev_len = 0
        for target in range(targets.shape[0]):
                curr_target = targets[target]
                curr_target = curr_target.decode('UTF-8') 
                curr_target = re.sub(' +', ' ', curr_target)
                curr_target = curr_target.replace(',','_')
                curr_target = curr_target.replace('.','_')
                curr_target = curr_target.replace(':','_')
                curr_target = curr_target.replace('-','_')
                curr_target = curr_target.replace('(','_')
                curr_target = curr_target.replace(')','_')
                curr_target = curr_target.replace('/','_')
                curr_target = curr_target.replace('/','_')
                curr_target = curr_target.replace('%','_')
                curr_target = curr_target.replace('^','_')
                curr_target = curr_target.replace('+','_')
                curr_target = curr_target.replace(' ','_')
                curr_target = curr_target.replace("'",'_')
                curr_target = re.sub('_+', '_', curr_target)

                if curr_target[-1]=='_': 
                        curr_target = curr_target.rstrip(curr_target[-1])

                if curr_target in data:
                        # changing the name of repeated key
                        while curr_target in data:
                                curr_target = curr_target + '_RPT'

                print(target, curr_target)
                data[curr_target] = scores[:,target]
                if target!=0 and prev_len == len(data.keys()):
                        print('\n\t\tWARNING!!! KEY EXITST\n\n\n')

                assert len(data.keys())!=target+5, '\n\t\tWARNING!!! KEY EXITST\n\n\n' 
                prev_len = len(data.keys())

        print(data.keys())
        df = pd.DataFrame(data)
        print('dictionary size: ', len(data))
        path = out_path + 'sad_2.csv'
        df.to_csv (path, index = False, header=True, sep ='\t')
        print('saved!')


import argparse

parser = argparse.ArgumentParser(description=' ========== h5 to bed SAD scores by Enrique Mondragon Estrada 2022 ==========', usage='%(prog)s')
parser.add_argument('-in', '--input', type=str, required=True, help='sad file', dest='sad_file')
parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')

args = parser.parse_args()

sad_file = args.sad_file
out_path = args.out_path

process_scores(sad_file)
