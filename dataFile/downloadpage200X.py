# 2001-2009

import urllib.request, urllib.parse
import re
import os
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

def shellghost(pdfLinkList, fileNames):
    for i in range(len(pdfLinkList)):
        os.system('curl ' + pdfLinkList[i] + ' --output ' + fileNames[i] + '.pdf')
        os.system('gs -sDEVICE=txtwrite -o ' + fileNames[i] + '.txt ' + fileNames[i] + '.pdf')


def main(name):
    #srcfile = 'dataFile/' + name
    code = name[-2:]
    f = open(name + '.txt', 'r')
    filename = name + 'resolve.txt'
    file1 = open(filename, 'w+')
    content = f.read()
    ten_digit = re.compile(r'(\d{4}\.\d{2}\.\d{2}\s+(?:\d{2})?)', flags=re.M)
    ten_digit_list = ten_digit.findall(content)
    array = []
    for i in range(len(ten_digit_list)):
        if ten_digit_list[i][0:2] == code:
            parsetwodigit(ten_digit_list, i, content, array)

    array = list(dict.fromkeys(array))
    for j in range(len(array)):
        temp = array[j]
        if len(temp) > 10:
            print(temp)

    file1.write(str(array))
    file1.close()
    f.close()

def special(name):
    f = open(name + '.txt', 'r')
    filename = name + 'resolve.txt'
    file1 = open(filename, 'w+')
    content = f.read()
    eight_digit = re.compile(r'(\d{4}\.\d{2}\.\d{2})\s{2,3}', flags=re.M)
    eight_digit_list = eight_digit.findall(content)
    array = []
    for i in range(len(eight_digit_list)):
        array.append(eight_digit_list[i])
    array = list(dict.fromkeys(array))
    result = []

    # if len(name) == 7:
    #     newcode = name[-2:]
    # else:
    #     code = name[-3:]
    #     newcode = code[0:2] + '0' + code[-1]
    for j in range(len(array)):
        temp = array[j].replace("\n", "")
        temp = temp.replace(" ", "")
        temp = temp.replace(".", "")
        result.append(temp)
        # if temp[0:4] == newcode and len(name) != 7:
        #     result.append(temp)
        # if temp[0:2] == newcode and len(name) == 7:
        #     result.append(temp)

    file1.write(str(result))
    file1.close()
    f.close()


def parsetwodigit(tendigitlist, i, content, array):
    if i == len(tendigitlist) - 1 :
        var = tendigitlist[i] + '(.+)'
    else:
        var = tendigitlist[i] + '(.+)' + tendigitlist[i + 1]
    pattern = re.compile(var, flags=re.M | re.DOTALL)
    pattern_list = pattern.findall(content)
    if len(pattern_list) == 0:
        print(tendigitlist[i])
    two_digit = re.compile('\s\s(\d{2})\s', flags=re.M)
    two_digit_list = two_digit.findall(pattern_list[0])
    temp = tendigitlist[i].replace("\n", "")
    temp = temp.replace(" ", "")
    temp = temp.replace(".", "")
    # special case for chapter 98
    if len(two_digit_list) == 0:
        array.append(temp)
    for j in range(len(two_digit_list)):
        if len(temp) == 10:
            array.append(temp)
            string = temp[0:8] + two_digit_list[j]
        else:
            string = temp + two_digit_list[j]
        array.append(string)

year = '09'
# todo: change according to the years
url = 'https://www.usitc.gov/tata/hts/bychapter/basic09.htm'
response = urllib.request.urlopen(url)
webContent = str(response.read())
pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/0900c\d{2,3}(?:_\d{1})?.pdf)', flags=re.M)
pdfLinkList = pdfLink.findall(webContent)
print(pdfLinkList)
for i in range(len(pdfLinkList)):
    pdfLinkList[i] = 'https://www.usitc.gov/' + pdfLinkList[i]

# todo: change according to the years
pdfshort = re.compile(r'\/(' + year + '00c\d{2,3})(?:_\d)?\.pdf', flags=re.M)
fileNames = pdfshort.findall(str(pdfLinkList))
# shellghost(pdfLinkList, fileNames)

for i in range(len(fileNames)):
    if fileNames[i][-2:] == '99':
        special(fileNames[i])
        print(fileNames[i])
    else:
        main(fileNames[i])
        print(fileNames[i])

# if __name__ == '__main__':
#     special('0200c99')
# 2001-2002 link
# url = 'https://www.usitc.gov/tata/hts/archive/' + year + '00/20' + year +'_basic_index.htm'
# pdfLink = re.compile(r'(\/tata\/hts\/archive\/' + year + '00\/'+ year + '00c\d{2,3}\.pdf)', flags=re.M)
# 2003 link
# url = 'https://www.usitc.gov/tata/hts/archive/20' + year +'/index.htm'
# pdfLink = re.compile(r'(\/publications\/tariff_chapters_2003basic\/' + year + '00c\d{2,3}\.pdf)', flags=re.M)
# 2004-2008
# url = 'https://www.usitc.gov/tata/hts/bychapter/_' + year +'00.htm'
# pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/' + year + '00c\d{2,3}\.pdf)', flags=re.M)
# 2009
# url = 'https://www.usitc.gov/tata/hts/bychapter/basic09.htm'
# pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/0900c\d{2,3}_\d{1}\.pdf)', flags=re.M)
# _number pdfshort = re.compile(r'\/(0900c\d{2,3}_\d{1})\.pdf', flags=re.M)
# for i in range(len(fileNames)):
#     main(fileNames[i])
# name = name[0:7]

