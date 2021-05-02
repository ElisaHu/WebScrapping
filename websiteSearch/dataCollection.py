import csv
import pandas as pd
my_csv = pd.read_csv('Revocation.csv')
column = my_csv['DOC case No.']
arr = column[1:].values
print(arr)
import _locale
# csvFile = open('Revocation.csv', 'w+')
# content = []
# with open('Revocation.csv', 'rt') as revocation:
#     csv_reader = csv.reader(revocation, delimiter=' ')
#     for row in csv_reader:
#         content.append(list(row[4]))

# url = 'https://www.usitc.gov/tata/hts/archive/' + year+ '00/19' + year +'_basic_index.htm'
