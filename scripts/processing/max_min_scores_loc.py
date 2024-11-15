#!/usr/bin/env python3

'''
Retrieves the max or min score for each participant by Enrique Mondragon Estrada 2022
'''

import numpy as np
import pandas as pd
import argparse

def read_data(sad_file):

    sad_df = pd.read_csv(sad_file, delimiter=',') # CHECK: '\t', ','

    id = sad_df['ID']
    chr_pos = sad_df['chrom_pos']
    SAD = sad_df.drop(['ID'], axis=1).drop(['chrom_pos'], axis=1)

    print(sad_df.shape, sad_df.keys())
    print(SAD, SAD.shape)

    print(id.shape[0])
    return SAD, id, chr_pos


def get_patients(SAD, id, chr_pos):
    '''
    creates 2 dictionaries 
    One in which every key is a patient and the values are lists of scores and the 
    other in which every key is a patient and the values are the chromosome and position
    '''
    patients_scores ={}
    patients_chrpos ={}
    for n in range(id.shape[0]):
        curr_id = id[n]
        if str(curr_id) not in patients_scores:
            patients_scores[str(curr_id)] = list()
            patients_chrpos[str(curr_id)] = list()
            patients_scores[str(curr_id)].append(SAD.iloc[n].values)
            patients_chrpos[str(curr_id)].append(chr_pos.iloc[n])
            print('does not exist, creating', curr_id)
        else:
            patients_scores[str(curr_id)].append(SAD.iloc[n].values)
            patients_chrpos[str(curr_id)].append(chr_pos.iloc[n])
            print('key exist, appending',curr_id)

    print('\nnumber of patients found is: ', len(patients_scores.keys()))

    num_targets = SAD.shape[1]
    print('num of target found is:', num_targets)
    return patients_scores, patients_chrpos, num_targets


def summary_statistics(patients):
    snps_per_patient = np.zeros(len(patients))
    patient_count = 0
    for patient in patients:
        sum_snps = 0
        for snp in range(len(patients[patient])):
            sum_snps = sum_snps + 1
        snps_per_patient[patient_count] = sum_snps
        patient_count = patient_count + 1
    print('mean: ', np.mean(snps_per_patient),'standard deviation', np.std(snps_per_patient))


def max_scores(patients, chrpos, num_targets, targets_names):

    for target in range(num_targets):
        targets_names[target] = targets_names[target] + '_max'

    max_sad = np.zeros((1,num_targets)) 
    max_sad_loc = pd.DataFrame(columns=targets_names)
    c=0
    for patient in patients:
        
        print('index: ',c , ' - ', 'patient: ', patient)
        c+=1

        max_row = np.zeros((1,num_targets))
        max_scores = {}
        max_loc = pd.DataFrame(0, index=range(1),columns=targets_names)
        
        # initialize max values
        for target in range(num_targets):
            curr_target = "{0}_max".format(target)
            max_scores[curr_target] = -float("inf")

        for snp in range(len(patients[patient])):
            snp_row = patients[patient][snp].reshape((1,num_targets)) 
            for target in range(num_targets):
                if snp_row[0,target]>=max_scores["{0}_max".format(target)]:
                    max_scores["{0}_max".format(target)] = snp_row[0,target]
                    max_loc.iloc[0, max_loc.columns.get_loc(targets_names[target])] = chrpos[patient][snp]

        for i in range(num_targets):
            max_row[0,i]=max_scores["{0}_max".format(i)]

        max_sad_loc = pd.concat([max_sad_loc, max_loc],
            ignore_index = True)
        #max_sad_loc = max_sad_loc.append(max_loc, ignore_index = True)

        max_sad = np.vstack((max_sad,max_row))
        
    max_sad = np.delete(max_sad,0, axis=0)
    print('max_sad is', max_sad)
    print('shape of max_sad is', max_sad.shape, 'equal to', len(patients))
    return max_sad, max_sad_loc


def min_scores(patients, chrpos, num_targets, targets_names):

    for target in range(num_targets):
        targets_names[target] = targets_names[target] + '_min'

    min_sad = np.zeros((1,num_targets)) 
    min_sad_loc = pd.DataFrame(columns=targets_names)
    c=0
    for patient in patients:

        print('index: ',c , ' - ', 'patient: ', patient)
        c+=1
        
        min_row = np.zeros((1,num_targets))
        min_scores = {}
        min_loc = pd.DataFrame(0, index=range(1),columns=targets_names) 

        for target in range(num_targets):
            curr_target = "{0}_min".format(target)
            min_scores[curr_target] = float("inf")

        for snp in range(len(patients[patient])):
            snp_row = patients[patient][snp].reshape((1,num_targets)) 
            for target in range(num_targets):
                if snp_row[0,target]<=min_scores["{0}_min".format(target)]:
                    min_scores["{0}_min".format(target)] = snp_row[0,target]
                    min_loc.iloc[0, min_loc.columns.get_loc(targets_names[target])] = chrpos[patient][snp]

        for i in range(num_targets):
            min_row[0,i]=min_scores["{0}_min".format(i)]

        min_sad_loc = pd.concat([min_sad_loc, min_loc],
            ignore_index = True)
        #min_sad_loc = min_sad_loc.append(min_loc, ignore_index = True)

        min_sad = np.vstack((min_sad,min_row))

    min_sad = np.delete(min_sad,0, axis=0)
    print('min_sad is', min_sad)
    print('shape of max_sad is', min_sad.shape, 'equal to', len(patients))
    return min_sad, min_sad_loc


def main():

    parser = argparse.ArgumentParser(description=' ========== Max and min score for each patient by Enrique Mondragon Estrada 2022 ==========', usage='%(prog)s')
    parser.add_argument('-in', '--input', type=str, required=True, help='sad file', dest='sad_file')
    parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')
    parser.add_argument('-stat', '--statistic', type=str, required=True, choices=['max', 'min'], help='statistic to compute', dest='stat')
    
    args = parser.parse_args()
    sad_file = args.sad_file
    out_path = args.out_path
    stat = args.stat

    SAD, id, chr_pos = read_data(sad_file)
    patients, chrpos, num_targets = get_patients(SAD, id, chr_pos)
    
    summary_statistics(patients)
    
    data = {'ID': patients.keys()
        }

    targets_names = list(SAD.columns.values)
    print('statistic to compute: ', stat)
    print(list(patients.keys()))
    if stat=='max': 
        max_sad, max_sad_loc = max_scores(patients, chrpos, num_targets, targets_names)
        print(max_sad_loc)
        
        for idx in range(num_targets):
            target = targets_names[idx]
            print('target is', target)
            print('score is', max_sad[:,idx].shape)
            data[target] = max_sad[:,idx]

        df2 = max_sad_loc
        name_out= '/max'
    
    
    elif stat=='min': 
        min_sad, min_sad_loc = min_scores(patients, chrpos, num_targets, targets_names)

        for idx in range(num_targets):
            target = targets_names[idx]
            print('target is', target)
            print('score is', min_sad[:,idx].shape)
            data[target] = min_sad[:,idx]
        
        df2 = min_sad_loc
        name_out= '/min'

    df1 = pd.DataFrame(data)
    print(df1)
    print(df2)

    path1 = out_path + name_out + '_sad.csv'
    path2 = out_path + name_out + '_sad_loc.csv'
    df1.to_csv (path1, index = False, header=True, sep ='\t')
    df2.to_csv (path2, index = False, header=True, sep ='\t')
    print('saved!')
    

if __name__ == "__main__":
    main()
