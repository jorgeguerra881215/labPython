# coding: utf-8
import pandas as pd
import numpy as np
df = pd.read_csv('/home/jtorres/Datasets/network-datasets/CTU-13.csv', sep = ' ')
df = df[df['proto'] == 'tcp']
df['len_seq'] = [len(seq) for seq in df['State']]
df = df[df['len_seq'] > 3]
df_bkp = df
df = df[(df['port'] == '80') | (df['port'] == '443')]
df['id'] = df.index.tolist()
#Setting aditional parameters
df['connection_id'] = df['ip_1'] + '-' + df['ip_2'] + '-' + df['port'] + '-' + df['proto']
df['title'] = df['Label']
df['uri'] = "http://www.mendeley.com"
df['creator'] = "Jhone Doe"
df['description'] = df['State']
df['collectionName'] = ""
df['keyword'] = ""
df['observation'] = ""
df['botprob'] = 0.5
df['botprob'] = "0.5"
df['confidence'] = "0.0"
df['facets'] = ""
df['att_vec'] = ""
df['eexcessURI'] = df['uri']
#df['cluster']=1
df_result = df[['id','title','uri','eexcessURI','creator','description','collectionName','keyword','observation','connection_id','cluster','botprob','confidence','facets','att_vec']]
df_result.to_json('/home/jtorres/Documents/dataset_http.json', orient='records')
