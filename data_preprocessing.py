import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

# Read csv file into pandas dataframe. Reading in train.csv
enzyme_train_df = pd.read_csv('novozymes-enzyme-stability-prediction/train.csv')
print('Train df')
print('---------------------------------------------------')
print(enzyme_train_df)

# Pre-update test
print('Pre-update test')
print('---------------------------------------------------')
print(enzyme_train_df.iloc[[68]])
print(enzyme_train_df.iloc[[69]])
print(enzyme_train_df.iloc[[973]])
print('---------------------------------------------------')





# Update train dataframe.  First we read in the train updates.  It gives us a list of indices we are modifying.
# This method is vectorized, and looks at the seq_id's that we modify in the train update
# and then modifies the original train df.  It excludes modifying the data_source column
enzyme_train_update_df = pd.read_csv('novozymes-enzyme-stability-prediction/train_updates_20220929.csv')
enzyme_train_df.iloc[enzyme_train_update_df['seq_id'], enzyme_train_df.columns != 'data_source'] = \
    enzyme_train_update_df.drop(columns=['data_source'])[:]

# Verifying that the changes worked
print('Train update verification')
print('---------------------------------------------------')
print(enzyme_train_df.iloc[[68]])
print(enzyme_train_df.iloc[[69]])
print(enzyme_train_df.iloc[[973]])
print('---------------------------------------------------')

# Read csv file into pandas dataframe.  Reading in test.csv
enzyme_test_df = pd.read_csv('novozymes-enzyme-stability-prediction/test.csv')
print(enzyme_test_df)

# Delete any rows that were left blank from the train updates
enzyme_train_df.dropna(subset=['protein_sequence'], inplace=True)

# Average length of protein sequence in train
print('Average train length: ', enzyme_train_df['protein_sequence'].apply(len).mean())

# Average length of protein sequence in test
print('Average test length: ', enzyme_test_df['protein_sequence'].apply(len).mean())

# Define feature and label columns
feature_cols = enzyme_train_df['seq_id', 'protein_sequence', 'pH']
label_col = enzyme_train_df['seq_id', 'tm']
