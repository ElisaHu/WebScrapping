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
    f = open(name + '.txt', 'r')
    code = name[-2:]
    filename = name + 'resolve.txt'
    file1 = open(filename, 'w+')
    content = f.read()
    ten_digit = re.compile(r'(\d{4}\.\d{2}\.\d{2}\s\s(?:\d{2})?)', flags=re.M)
    ten_digit_list = ten_digit.findall(content)
    array = []
    for i in range(len(ten_digit_list)):
        if len(ten_digit_list[i]) == 12:
            if i < len(ten_digit_list) - 1:
                parsetwodigit(ten_digit_list, i, content, array)

            if i == len(ten_digit_list) - 1:
                parsetwodigitedge(ten_digit_list, i, content, array)

        else:
            array.append(ten_digit_list[i])

    array = list(dict.fromkeys(array))
    result = []
    for j in range(len(array)):
        temp = array[j].replace("\n", "")
        temp = temp.replace(" ", "")
        temp = temp.replace(".", "")
        if temp[0:2] == code:
            result.append(temp)

    file1.write(str(result))
    file1.close()
    f.close()

def special(name):
    f = open(name + '.txt', 'r')
    filename = name + 'resolve.txt'
    file1 = open(filename, 'w+')
    content = f.read()
    eight_digit = re.compile(r'(\d{4}\.\d{2}\.\d{2})\s\s', flags=re.M)
    eight_digit_list = eight_digit.findall(content)
    array = []
    for i in range(len(eight_digit_list)):
        array.append(eight_digit_list[i])
    array = list(dict.fromkeys(array))
    result = []

    if len(name) == 7:
        newcode = name[-2:]
    else:
        code = name[-3:]
        newcode = code[0:2] + '0' + code[-1]
    for j in range(len(array)):
        temp = array[j].replace("\n", "")
        temp = temp.replace(" ", "")
        temp = temp.replace(".", "")
        if temp[0:4] == newcode and len(name) != 7:
            result.append(temp)
        if temp[0:2] == newcode and len(name) == 7:
            result.append(temp)

    file1.write(str(result))
    file1.close()
    f.close()


def parsetwodigit(tendigitlist, i, content, array):
    var = tendigitlist[i] + '(.+)' + tendigitlist[i + 1]
    pattern = re.compile(var, flags=re.M | re.DOTALL)
    pattern_list = pattern.findall(content)
    two_digit = re.compile('\ (\d{2})\ ', flags=re.M)
    two_digit_list = two_digit.findall(pattern_list[0])
    # special case for chapter 98
    if len(two_digit_list) == 0:
        array.append(tendigitlist[i])
    for j in range(len(two_digit_list)):
        string = tendigitlist[i] + two_digit_list[j]
        array.append(string)


# Define a function to parse two digit edge case
def parsetwodigitedge(tendigitlist, i, content, array):
    var = tendigitlist[i] + '(.+)'
    pattern = re.compile(var, flags=re.M | re.DOTALL)
    patternlist = pattern.findall(content)
    twodigit = re.compile('\ (\d{2})\ ', flags=re.M)
    twodigitlist = twodigit.findall(patternlist[0])
    for j in range(len(twodigitlist)):
        string = tendigitlist[i] + twodigitlist[j]
        array.append(string)
year = '04'
# todo: change according to the years
url = 'https://www.usitc.gov/tata/hts/bychapter/_' + year +'00.htm'
response = urllib.request.urlopen(url)
webContent = str(response.read())
pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/' + year + '00c\d{2,3}\.pdf)', flags=re.M)

pdfLinkList = pdfLink.findall(webContent)
for i in range(len(pdfLinkList)):
    pdfLinkList[i] = 'https://www.usitc.gov/' + pdfLinkList[i]

# todo: change according to the years
pdfshort = re.compile(r'\/(' + year + '00c\d{2,3})\.pdf', flags=re.M)
fileNames = pdfshort.findall(str(pdfLinkList))
# shellghost(pdfLinkList, fileNames)

for i in range(len(fileNames)):
    if fileNames[i][-2:] == '99':
        special(fileNames[i])
    elif len(fileNames[i]) == 7:
        main(fileNames[i])
    else:
        special(fileNames[i])

# if __name__ == '__main__':
#     special('0200c99')

# 2003 link
# url = 'https://www.usitc.gov/tata/hts/archive/20' + year +'/index.htm'
# pdfLink = re.compile(r'(\/publications\/tariff_chapters_2003basic\/' + year + '00c\d{2,3}\.pdf)', flags=re.M)
# 2004-2008
# url = 'https://www.usitc.gov/tata/hts/bychapter/_' + year +'00.htm'
# pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/' + year + '00c\d{2,3}\.pdf)', flags=re.M)
# 2009
# url = 'https://www.usitc.gov/tata/hts/bychapter/basic' + year +'.htm'
# pdfLink = re.compile(r'(\/publications\/docs\/tata\/hts\/bychapter\/0900c\d{2,3}_\d{1}\.pdf)', flags=re.M)
# _number pdfshort = re.compile(r'\/(0900c\d{2,3}_\d{1})\.pdf', flags=re.M)
# for i in range(len(fileNames)):
#     main(fileNames[i])
# name = name[0:7]

