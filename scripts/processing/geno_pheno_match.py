#!/usr/bin/env python3

'''
Filters participants that have genotype (variant scores) and phenotype 
(sulcal pattern coefficients) data by Enrique Mondragon Estrada 2022
'''

def filter_data(sad_file, sulcal_file, out_path):
    
    import pandas as pd

    sulcal_df = pd.read_csv(sulcal_file) # CHECK: '\t', ','
    sad_df = pd.read_csv(sad_file, delimiter='\t')
    print(sulcal_df)
    print(sad_df)

    sad_patients = sad_df['ID']
    sulcal_patients = sulcal_df['ID']
    c=0
    patients_match = []
    for sad_patient in sad_patients:
        for sulcal_patient in sulcal_patients:
            if sad_patient == sulcal_patient:
                c = c+1
                patients_match.append(sad_patient)
                print('patient: ', sad_patient, 'has sulcal pattern data')

    print(c, 'patients have sulcal data') 
    print('list is', patients_match)

    sad_df_match = sad_df[sad_df['ID'].isin(patients_match)]
    sulcal_df_match = sulcal_df[sulcal_df['ID'].isin(patients_match)]


    sad_path = out_path + 'sad_match.csv'
    sulcal_path = out_path + 'sulcal_match.csv'

    sad_df_match.to_csv (sad_path, index = False, header=True, sep ='\t')
    sulcal_df_match.to_csv (sulcal_path, index = False, header=True, sep ='\t')
    print('saved!')


import argparse

parser = argparse.ArgumentParser(description=' ========== Filter patients with genotype and phenotype data by Enrique Mondragon Estrada 2022 ==========', usage='%(prog)s')
parser.add_argument('-sad', '--sad_file', type=str, required=True, help='sad file', dest='sad_file')
parser.add_argument('-sulcal', '--sulcal_file', type=str, required=True, help='sad file', dest='sulcal_file')
parser.add_argument('-out', '--output', type=str, required=True, help='output directory', dest='out_path')

args = parser.parse_args()
sad_file = args.sad_file
sulcal_file = args.sulcal_file
out_path = args.out_path

filter_data(sad_file, sulcal_file, out_path)
