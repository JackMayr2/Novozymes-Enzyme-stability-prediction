import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

pd.set_option('display.max_columns', None)

# Read csv file into pandas dataframe. Reading in train.csv
enzyme_train_df = pd.read_csv('novozymes-enzyme-stability-prediction/train.csv')
# print('Train df')
# print('---------------------------------------------------')
# print(enzyme_train_df)

# Pre-update test
# print('Pre-update test')
# print('---------------------------------------------------')
# print(enzyme_train_df.iloc[[68]])
# print(enzyme_train_df.iloc[[69]])
# print(enzyme_train_df.iloc[[973]])
# print('---------------------------------------------------')

# Update train dataframe.  First we read in the train updates.  It gives us a list of indices we are modifying.
# This method is vectorized, and looks at the seq_id's that we modify in the train update
# and then modifies the original train df.  It excludes modifying the data_source column
enzyme_train_update_df = pd.read_csv('novozymes-enzyme-stability-prediction/train_updates_20220929.csv')
enzyme_train_df.iloc[enzyme_train_update_df['seq_id'], enzyme_train_df.columns != 'data_source'] = \
    enzyme_train_update_df.drop(columns=['data_source'])[:]

# Verifying that the changes worked
# print('Train update verification')
# print('---------------------------------------------------')
# print(enzyme_train_df.iloc[[68]])
# print(enzyme_train_df.iloc[[69]])
# print(enzyme_train_df.iloc[[973]])
# print('---------------------------------------------------')

# Read csv file into pandas dataframe.  Reading in test.csv
enzyme_test_df = pd.read_csv('novozymes-enzyme-stability-prediction/test.csv')
# print(enzyme_test_df)

# Delete any rows that were left blank from the train updates
enzyme_train_df.dropna(subset=['protein_sequence'], inplace=True)

# Average length of protein sequence in train
print('Average train length: ', enzyme_train_df['protein_sequence'].apply(len).mean())

# Average length of protein sequence in test
print('Average test length: ', enzyme_test_df['protein_sequence'].apply(len).mean())

# Define feature and label columns
feature_cols = enzyme_train_df.filter(['seq_id', 'protein_sequence', 'pH'], axis=1)
label_col = enzyme_train_df.filter(['seq_id', 'tm'], axis=1)

# Tokenize the protein sequences
# First, we need to aggregate all the sequences together so that their encodings are all the same.
agg_protein_sequences = ''.join(feature_cols["protein_sequence"].astype(str))
print('total protein sequence length: ', len(agg_protein_sequences))
print('average protein sequence length: ', len(agg_protein_sequences) / len(feature_cols.index))

# tokenize the aggregate of protein sequences
tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)  # default is word level
tokenizer.fit_on_texts([agg_protein_sequences])
# returns the number of distinct characters
max_id = len(tokenizer.word_index)
print('max ID: ', max_id)

# Now we want to encode each of the protein sequences in a column
feature_cols['tokenized_protein_sequence'] = feature_cols['protein_sequence'].apply(
    lambda x: (tokenizer.texts_to_sequences([x])))
# print(feature_cols.head())
# From the protein sequence and pH of the enzyme, we want to be able to predict the numerical output tm (melting temperature.
