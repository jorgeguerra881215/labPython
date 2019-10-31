# coding: utf-8
print('Starting ...')
print('Importing libraries')
import pandas as pd
import numpy as np
print('Loading dataset')

#Specify the location to load the dataset
data_location = '/home/jtorres/Python/pandas/data/capture20110810.binetflow.labeled'
df = pd.read_csv(data_location, sep='|')
df['length'] = df.apply(lambda row:len(row.State),axis = 1)

#Using only connections with more than 4 characters
df = df[df['length']>4]
df['short_label'] = df.apply(lambda row:str.split(row.label,'-')[1],axis = 1)
aux_df = df[['State','short_label']]
aux_df.columns = ['State', 'Label']
aux_df['Words'] = aux_df.apply(lambda row: ' '.join([row.State[i:i+5] for i in range(0,len(row.State)-5+1)]), axis = 1)

#Replacing in words the punctuation symbols by letters. This modification is to avoid deal with punctuation symbols in the steming process.
aux_df['Words'] = aux_df.apply(lambda row: row.Words.replace('.','p'),axis=1 )
aux_df['Words'] = aux_df.apply(lambda row: row.Words.replace(',','j'),axis=1 )
aux_df['Words'] = aux_df.apply(lambda row: row.Words.replace('+','k'),axis=1 )
aux_df['Words'] = aux_df.apply(lambda row: row.Words.replace('*','q'),axis=1 )
aux_df['Words'] = aux_df.apply(lambda row: row.Words.replace('0','o'),axis=1 )

resultant_df = aux_df[['Words', 'Label']]
print('Creating resultant dataset file')
resultant_df.to_csv('sc_documents.txt', sep='|')
print('DONE')
