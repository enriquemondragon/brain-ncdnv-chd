#!/usr/bin/env python3

'''
Bonferroni correction applied to statistical tests with functional scores by Enrique Mondragon Estrada 2023
'''

def bonferroni_correction(test_file, out_path, alpha):
    
    import numpy as np
    import pandas as pd

    test = pd.read_csv(test_file, delimiter='\t')
    print(test)

    num_targets = len(test.index)
    num_hypothesis = num_targets*2
    alpha_new = alpha / num_hypothesis

    FWER = 1 - (1 - alpha)**num_hypothesis # Family Wise Error Rate
    print('\n',parser.description)
    print('alpha value: ', alpha)
    print('Number of hypothesis: ', num_hypothesis)
    print('Probability that we commit a type I error: ', FWER)

    print('alpha value with Bonferroni correction: ', alpha_new)

    count = 0
    stat_sgfnt = pd.DataFrame(columns=['target', 'statistic_l', 'pvalue_l', 'statistic_h', 'pvalue_h', 'summary'])
    for idx in range(num_targets):
        target = test.iloc[idx]['target']
        pvalue_l = test.iloc[idx]['pvalue_l']
        statistic_l = test.iloc[idx]['statistic_l']
        pvalue_h = test.iloc[idx]['pvalue_h']
        statistic_h = test.iloc[idx]['statistic_h']
        
        if pvalue_l <= alpha_new and pvalue_h > alpha_new:
            print('target:', target, 'pvalue:',pvalue_l)
            df_temp = {'target': target, 'statistic_l': statistic_l, 'pvalue_l': pvalue_l,
                       'statistic_h': None, 'pvalue_h': None, 'summary': 1}
            df_temp = pd.DataFrame(df_temp, index=[0])
            stat_sgfnt = pd.concat([stat_sgfnt, df_temp],
            ignore_index = True)
            count = count + 1
        elif pvalue_l > alpha_new and pvalue_h <= alpha_new:
            print('target:', target, 'pvalue:',pvalue_h)
            df_temp = {'target': target, 'statistic_l': None, 'pvalue_l': None,
                       'statistic_h': statistic_h, 'pvalue_h': pvalue_h, 'summary': 1}
            df_temp = pd.DataFrame(df_temp, index=[0])
            stat_sgfnt = pd.concat([stat_sgfnt, df_temp],
            ignore_index = True)
            count = count + 1
        elif pvalue_l <= alpha_new and pvalue_h <= alpha_new:
            print('target:', target, 'pvalue:',pvalue_l, pvalue_h)
            df_temp = {'target': target, 'statistic_l': statistic_l, 'pvalue_l': pvalue_l,
                       'statistic_h': statistic_h, 'pvalue_h': pvalue_h, 'summary': 2}
            df_temp = pd.DataFrame(df_temp, index=[0])
            stat_sgfnt = pd.concat([stat_sgfnt, df_temp],
            ignore_index = True)
            count = count + 1

    print(count, 'targets from', num_targets, 'are stat_sgfnt')

    print(stat_sgfnt)
    path = out_path + 'stat_sgfnt_bonferroni.csv'
    stat_sgfnt.to_csv (path, index = False, header=True, sep ='\t')
    print('saved!')


import argparse

parser = argparse.ArgumentParser(description=' ========== Bonferroni correction applied to statistical tests with functional scores by Enrique Mondragon Estrada 2023 ==========', usage='%(prog)s')
parser.add_argument('-in', '--input', type=str, required=True, help='test file', dest='test_file')
parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')
parser.add_argument('-a', '--alpha', type=float, default=0.05, help='alpha value', dest='alpha')

args = parser.parse_args()
test_file = args.test_file
out_path = args.out_path
alpha = args.alpha

bonferroni_correction(test_file, out_path, alpha)