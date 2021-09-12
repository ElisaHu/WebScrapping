import pandas as pd
import os
from os import listdir
from os.path import join
import csv
from functools import reduce

# todo: gets all the sorted csv files
# path = os.path.abspath("..\\caselist")
path ="..\\caselist"
onlyfiles = []
for f in listdir(path):
    onlyfiles.append(join(path, f))
column = set()
for eachfilepath in onlyfiles:
    with open(eachfilepath, 'rb') as f:
        firstcolumn = f.readline()
        firstcolumndecode = firstcolumn.decode('utf-8').split(',')
        for eachname in firstcolumndecode:
            column.add(eachname)

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
            df = pd.DataFrame(all)
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            new_name = 'new ' + eachfilepath.split('\\')[-1]
            df.to_csv(new_name, index=False)
    with open(new_name, newline="", encoding='UTF-8') as csv_file:
        reader = csv.DictReader(csv_file)
        headers = sorted(reader.fieldnames)
        # for each_head_index in range(len(headers)):
        #     headers[each_head_index] = headers[each_head_index].replace('\r\n', '')
        header_values = ",".join(header.replace('\r\n', '') for header in headers)

        file = header_values + '\n'

        for line in reader:
            row = sorted(line.items())
            values = map(lambda v: v[1], row)
            eachrowsorted = ",".join(v.replace(',', '') for v in values)
            file += eachrowsorted + "\n"
        sorted_name = str(new_name) + "_sorted.csv"

        with open(sorted_name, "w",  encoding='utf-8') as sorted_file:
            sorted_file.write(file)
            sorted_file.close()

path2 ="."
allfiles = []
all_sorted_files = []
for f in listdir(path2):
    allfiles.append(join(path2, f))
for eachfilepath in allfiles:
    if 'sorted' in eachfilepath:
        all_sorted_files.append(eachfilepath)

# print(all_sorted_files)
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_sorted_files ])
#export to csv
combined_csv.to_csv("combined_csv.csv", index=False, encoding='UTF-8')

