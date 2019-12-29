import os
import pandas as pd
import glob, csv
import numpy as np

path = '/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/normalizedwordgroups/'
def concat_df():
    df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(path, "*.csv"))))
    df = df.replace('', np.nan)
    df = df.replace(np.nan, -1.0)
    print(df.columns)
    df.to_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/' + 'DataForClassification.csv', sep=',', encoding='utf-8', index=False)

def clean_df_remove_nullfeaturerows():
    data = pd.read_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/DataForClassification.csv')
    data_new = data
    for column in data.columns:
        print(column)
        data_new = data_new.drop(data_new.loc[data_new[column] == -1].index)
        data_new = data_new.drop(data_new.loc[data_new[column] == -1.0].index)
    data_new.to_csv('/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/DataForClassification.csv', sep=',', encoding='utf-8', index=False)

concat_df()
clean_df_remove_nullfeaturerows()
