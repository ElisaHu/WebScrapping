import csv

import pandas as pd
import urllib.request, urllib.parse
import re
import requests
import lxml

# get numpy array from csv file
my_csv = pd.read_csv('Overall.csv')
column = my_csv['DOCNo']
DOCarray = column[1:].values
productColumn = my_csv['Product']
productArray = productColumn[1:].values


def AntiDumping(DOC, product):
    # get the website link, read content from it
    url = 'https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=' + DOC
    response = urllib.request.urlopen(url)
    webContent = str(response.read())
    for pageNum in range(2, 10):
        nextPage = url + '&page=' + str(pageNum)
        response = urllib.request.urlopen(nextPage)
        thisPageWebContent = str(response.read())
        errorCheckFormat = re.compile(r'(No documents were found.)', flags=re.M)
        errorCheck = errorCheckFormat.findall(thisPageWebContent)
        if (errorCheck):
            break;
        print(pageNum)
        webContent += thisPageWebContent
    # print(webContent)
    webLinkFormat = re.compile(r'"(https://www.federalregister.gov/documents/\d+.+?)"', flags=re.M)
    webLinkList = webLinkFormat.findall(webContent)
    # print(webLinkList)
    print(len(webLinkList))
    initiation = []
    activation = []
    revocation = []
    for i in webLinkList:
        productLink = product.replace(' ', '-').lower()
        if productLink in i:
            longlink = urllib.request.urlopen(i)
            longwebContent = str(longlink.read())
            print(longwebContent)
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            if 'Review' in title:
                continue;
            if 'Preliminary' in title:
                continue;
            if 'Notice' in title:
                continue;
            print(title)
            if 'Initiation of Antidumping Duty' in title:
                initiation.append(i)
            if 'Antidumping Duty Orders' in title:
                activation.append(i)
                # html = requests.get(url).content
                # df_list = pd.read_html(html)
                # df = df_list[-1]
                # print(df)
            if 'Revocation of Antidumping' in title:
                revocation.append(i)
    if len(initiation) == 0 or len(activation) == 0:
        print('take a look! we do not have initiation or activation in this product?')
    if len(activation) > 0:
        # we should only have 1 activation file per product
        # find DOC No., Year, Month, Date, HS1, HS2, HS3, HS4, HS5, HS6, HS7, Product, Country, Exporter, ExpAltNm, Producer, PdAltNm,  ProducerID,  AD_CVD, Dumping Margin, Cash Deposit, Action, Source
        dataFormat = re.compile(r'Publication Date:.+documents\/(.+?)">',
                flags=re.M)
        title = dataFormat.findall(longwebContent)[0]

    # print("initiation")
    # print(initiation)
    # print("activation")
    # print(activation)
    # print("revocation")
    # print(revocation)
AntiDumping('A-201-842', 'Large Residential Washers')

# todo: change this function to match antidumping duty
# def Countervailing(DOC, product):
#     # get the website link, read content from it
#     url = 'https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=' + DOC
#     response = urllib.request.urlopen(url)
#     webContent = str(response.read())
#     for pageNum in range(2, 10):
#         nextPage = url + '&page=' + str(pageNum)
#         response = urllib.request.urlopen(nextPage)
#         thisPageWebContent = str(response.read())
#         errorCheckFormat = re.compile(r'(No documents were found.)', flags=re.M)
#         errorCheck = errorCheckFormat.findall(thisPageWebContent)
#         if (errorCheck):
#             break;
#         print(pageNum)
#         webContent += thisPageWebContent
#     # print(webContent)
#     webLinkFormat = re.compile(r'"(https://www.federalregister.gov/documents/\d+.+?)"', flags=re.M)
#     webLinkList = webLinkFormat.findall(webContent)
#     print(webLinkList)
#     print(len(webLinkList))
#     for i in webLinkList:
#         if "Initiation" in i and "Initiation" in i:


# iterating over each DOC Number
# for index in range(0, len(DOCarray)):
#     # create one csv file for each DOC case
#     currcsvname = productArray[index]
#     csvFile = open(currcsvname + '.csv', 'w+')
#     csvFile.write(["DOC No., Year, Month, Date, HS1, HS2, HS3, HS4, HS5, HS6, HS7, Product, Country, Exporter, ExpAltNm, Producer, PdAltNm,  ProducerID,  AD_CVD, Dumping Margin, Cash Deposit, Action, Source"])
#     # get the type: AD/CVD -- first char in a string
#     type = DOCarray[index][0]
#     if (type == 'A'):
#         AntiDumping(DOCarray[index], productArray[index], csvFile)
#     elif (type == 'C'):
#         Countervailing(DOCarray[index], productArray[index], csvFile)
#     else:
#         print(DOCarray[index])

    # df = pd.read_csv("example.csv", header=None)
    # df.to_csv("example.csv", header=["Letter", "Number", "Symbol"], index=False)

# --------unworked code------------------------------------------------------
# csvFile = open('Revocation.csv', 'w+')
# content = []
# with open('Revocation.csv', 'rt') as revocation:
#     csv_reader = csv.reader(revocation, delimiter=' ')
#     for row in csv_reader:
#         content.append(list(row[4]))

