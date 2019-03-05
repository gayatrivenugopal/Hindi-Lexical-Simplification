import pandas as pd
import numpy as np
import csv

def remove_duplicates(file):
	"""
	Removes duplicate values from the row number and decrements the corresponding count
	"""
	df = pd.read_csv(file, encoding='utf-8')
	new_df = df
	for index,row in df.iterrows():
		count = row['Count']
		rows = row['Row'].split(',')
		#remove duplicates and reduce count
		new_rows = []
		for value in rows:
			if not value in new_rows:
				new_rows.append(value)
			else:
				count = count - 1
		new_df.at[index,'Count'] = count
		#df.at[index,'Row'] = '"' + ','.join(new_rows) + '"'
		new_df.at[index,'Row'] = ','.join(new_rows)
	new_df.to_csv(file.replace("Native/", "Native/clean_"), encoding='utf-8', index=False)

remove_duplicates('Native/nativepilot.csv')
remove_duplicates('Non Native/nonnativepilot.csv')