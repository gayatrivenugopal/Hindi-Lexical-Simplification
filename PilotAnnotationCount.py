import xlrd
import re
import pandas as pd

def read_file(path):
    df = pd.DataFrame(index = range(0,56), columns=['Word', 'Count', 'Row'])
    book = xlrd.open_workbook(path,encoding_override='cp1252')
    sheet = book.sheet_by_index(0)
    i = 0
    for rowno in range(0, 56):
       # print(rowno)
        hindi_cols = (19, 22, 24, 25, 27, 30, 32, 33, 36, 37, 40, 43, 46, 48, 49, 50, 51, 52, 53, 54, 55)
        for cellno in hindi_cols:
            cellvalue = str(sheet.cell(rowno, cellno).value)
            words = re.split('[\s+,]', cellvalue)
            for word in words:
                row = df.loc[df['Word'] == word.strip()]
                #print(len(row.index))
                if len(row.index) != 0:
                    df.loc[df['Word'] == word.strip(),'Count'] = int(row['Count']) + 1
                    #print("ROW")
                    #print(row)
                    df.loc[df['Word'] == word.strip(),'Row'] = row['Row'] + "," + str(rowno)
                else:
                    df.loc[i] = [word.strip(), 1, str(rowno)]                    
                    i = i + 1
    #print(df)
    df.to_csv('nativepilot.csv', header=['Word', 'Count', 'Row'], index=range(0,56),sep=',', mode='a', encoding = 'utf-8')

read_file("T:\Research\Ph.D\Ph.D\Work\HWN API\JHWNL_1_2\Final Corpora\Experiment Files\Hindi.xls.xlsx")