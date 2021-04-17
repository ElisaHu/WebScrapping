
from zipfile import ZipFile
import re

csv = "Year, hs10" + "\n"

csvFile = open('overallData.csv', 'w+')
for i in range(1994, 2009+1):
    filename = str(i) + ".zip"
    with ZipFile(filename, 'r') as zip:
       files = zip.filelist
       for file in files:
           if "resolve" in file.filename:
               array = str(zip.read(file))
               sectionsPattern = re.compile(r'(\d+)', flags=re.M)
               sections = sectionsPattern.findall(array)
               for section in sections:
                   csv += str(i) + ", " + section + "\n"

csvFile.write(csv)