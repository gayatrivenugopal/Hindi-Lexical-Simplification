import os
import pandas as pd

path = '/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/finalwordgroups/'
norm_path = '/opt/PhD/Work/JHWNL_1_2/Data/CleanedData/normalizedwordgroups/'

for file in sorted(os.listdir(path)):
    print(file)
    df = pd.read_csv(path + file)
    #print(df)
    #del df['id']
    print(df.head())
    features_to_normalize = ['length','n_synsets','n_synonyms','n_avg_synonyms','n_consonants','n_vowels','n_hypernyms','n_avg_hypernyms','n_hyponyms','n_avg_hyponyms','n_consonantconjuncts','n_syllables', 'frequency']
    df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))
    #print(df)
    df.to_csv(norm_path + file, sep=',', encoding='utf-8', index=False)

