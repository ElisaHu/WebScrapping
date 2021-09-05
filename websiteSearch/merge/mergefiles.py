import pandas as pd
import os
from os import listdir
from os.path import join
import csv

path = os.path.abspath("..\\caselist")
print(path)
onlyfiles = []
for f in listdir(path):
    onlyfiles.append(join(path, f))
column = set()
for eachfilepath in onlyfiles:
    print(eachfilepath)

    with open(eachfilepath, 'rb') as f:
        firstcolumn = f.readline()
        firstcolumndecode = firstcolumn.decode('utf-8').split(',')
        for eachname in firstcolumndecode:
            column.add(eachname)

print(column)
print(len(column))

column = column - {'1'} - {'2'} - {'Unnamed: 0'}
df_overall = pd.DataFrame()
for eachfilepath in onlyfiles:
    with open(eachfilepath, 'rb') as f2:
        firstcolumn2 = f2.readline().decode('utf-8').split(',')
        columnnotinfile = column - set(firstcolumn2)

        with open(eachfilepath, 'r', encoding='UTF-8') as csvinput:
            reader = csv.reader(csvinput)
            all = []
            row0 = next(reader)
            row0 = row0 + list(columnnotinfile)
            all.append(row0)
            for eachrow in reader:
                eachrow = eachrow + ([''] * len(columnnotinfile))
                all.append(eachrow)
            print(all)
    df = pd.DataFrame(all)
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df.reindex(sorted(df.columns), axis=1)
    if df_overall.empty:
        df_overall = df
    else:
        df_overall.merge(df, on = list(column))

df_overall.to_csv('all_file_merge.csv', index=False)
            # with open(eachfilepath, 'w') as f3:
            #     writer = csv.writer(f3)
            #     writer.writerows(all)