#!/usr/bin/env python3

'''
One-sided Mann-Whitney U-test for variant scores by Enrique Mondragon Estrada 2023
'''

def mannwhitneyu_test(chd_file, non_chd_file, out_path):
    
    import pandas as pd
    import numpy as np
    from scipy import stats

    sad_chd_df = pd.read_csv(chd_file, delimiter='\t')
    sad_non_df = pd.read_csv(non_chd_file, delimiter='\t')
    
    SAD_chd = sad_chd_df.drop(['chrom'], axis=1).drop(['pos'], axis=1).drop(['ID'], axis=1).drop(['ref'], axis=1).drop(['alt'], axis=1)
    SAD_non = sad_non_df.drop(['chrom'], axis=1).drop(['pos'], axis=1).drop(['ID'], axis=1).drop(['ref'], axis=1).drop(['alt'], axis=1)

    targets = SAD_chd.columns

    print('\n',parser.description)
    print('CHD N: ', SAD_chd.shape[0])
    print('non-CHD N: ', SAD_non.shape[0])
    print('Mann-Withney U test will be performed on: ', SAD_chd.shape[1], 'targets\n')

    assert SAD_chd.shape[1]==SAD_non.shape[1], ' files should have scores for the same number of epigenomic targets (bigwig files)'
    
    num_targets = SAD_chd.shape[1]

    print('targets are: ', targets)

    df = pd.DataFrame(columns = ['target', 'statistic_l', 'pvalue_l','statistic_h', 'pvalue_h'])
    
    SAD_chd = np.array(SAD_chd,dtype= np.float64) 
    SAD_non = np.array(SAD_non,dtype= np.float64)
    
    for target in range(num_targets):

        CHD_target = SAD_chd[:,target]
        NON_target = SAD_non[:,target]

        chd_q3 = np.quantile(CHD_target, 0.75)
        chd_q1 = np.quantile(CHD_target, 0.25)

        non_q3 = np.quantile(NON_target, 0.75)
        non_q1 = np.quantile(NON_target, 0.25)

        high_chd = CHD_target[CHD_target > chd_q3]
        low_chd = CHD_target[CHD_target < chd_q1]

        high_non = NON_target[NON_target > non_q3]
        low_non = NON_target[NON_target < non_q1]

        result1 = stats.mannwhitneyu(low_chd, low_non, alternative='less')
        print(targets[target], " low ", result1.statistic, result1.pvalue)
        result2 = stats.mannwhitneyu(high_chd, high_non, alternative='greater')
        print(targets[target], " high ", result2.statistic, result2.pvalue)

        temp = {'target' : targets[target], 'statistic_l' : result1.statistic, 'pvalue_l' : result1.pvalue,
                'statistic_h' : result2.statistic, 'pvalue_h' : result2.pvalue}
        temp = pd.DataFrame(temp, index=[0])
        df = pd.concat([df, temp],
            ignore_index = True)
        
    print(df)
    path = out_path + 'manntest_split.csv'
    df.to_csv (path, index = False, header=True, sep ='\t')



import argparse

parser = argparse.ArgumentParser(description=' ========== Mann-Whitney U test for variant scores by Enrique Mondragon Estrada 2023 ==========', usage='%(prog)s')
parser.add_argument('-chd', '--CHD_SAD', type=str, required=True, help='sad chd', dest='sad_chd')
parser.add_argument('-non', '--NON_CHD_SAD', type=str, required=True, help='sad non-chd', dest='sad_non_chd')
parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')
args = parser.parse_args()

chd_file = args.sad_chd
non_chd_file = args.sad_non_chd
out_path = args.out_path

mannwhitneyu_test(chd_file, non_chd_file, out_path)
