import os
import pandas as pd


path = '/opt/PhD/Work/JHWNL_1_2/Data/Frequency/'
final_df = pd.DataFrame()
add = 0
for file in sorted(os.listdir(path)):
    print(file)
    df = pd.read_csv(path + file)
    if final_df.empty:
        final_df = df
    else:
        final_df = pd.merge(final_df,df,how='outer').groupby(['word'],as_index=False)['frequency'].sum()
final_df.to_csv(path + 'frequencies.csv', sep=',', encoding='utf-8', index=False)
