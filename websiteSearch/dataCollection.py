import csv
import math

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
            if 'Initiation of Antidumping Duty' in title:
                print(title)
                initiation.append(i)
                initiation_source = i
                initiation_action = 'initiation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})',flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                initiation_year = dateString[:4]
                initiation_month = dateString[5:7]
                initiation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n',flags=re.M)
                initiation_FedReg = FedRegFormat.findall(longwebContent)[0]
                initiation_petitioners = []
                petitionerFormat = re.compile(r'by\s(.+)\s\(“the petitioner”\)',flags=re.M)
                initiation_petitioners.append(petitionerFormat.findall(longwebContent)[0])
            if 'Antidumping Duty Orders' in title:
                print(title)
                activation.append(i)
                activation_source = i
                activation_action = 'activation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})',
                                        flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                activation_year = dateString[:4]
                activation_month = dateString[5:7]
                activation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n',
                                          flags=re.M)
                activation_FedReg = FedRegFormat.findall(longwebContent)[0]
                html = requests.get(i).content
                df_list = pd.read_html(html)
                df = pd.DataFrame(df_list[-1])
                # fill country name
                last = ''
                countries = []
                for i in range(len(df['Country'])):
                    curr = df['Country'][i]
                    if isinstance(curr, str):
                        last = curr
                        countries.append(curr)
                    else:
                        countries.append(last)
                df['Country'] = countries
                df['Year'] = [activation_year]*len(df)
                df['Month'] = [activation_month]*len(df)
                df['Date'] = [activation_date]*len(df)
                df['FedReg'] = [activation_FedReg]*len(df)
                df['AD/CVD'] = ['AD']*len(df)
                df['Action'] = [activation_action]*len(df)

                HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                activation_HScodeList = list(HScodeFormate.findall(longwebContent))
                if len(activation_HScodeList) == 5:
                    for i in range(0, len(activation_HScodeList)):
                        df['HS' + str(i+1)] = [activation_HScodeList[i]]*len(df)
                if len(activation_HScodeList) == 6:
                    df['HS' + '3'] = ''
                    for i in range(0, len(activation_HScodeList)):
                        if i < 3:
                            df['HS' + str(i+1)] = [activation_HScodeList[i]]*len(df)
                        if i >= 3:
                            df['HS' + str(i+2)] = [activation_HScodeList[i]]*len(df)
                if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:
                    print('irregular HScode')
                    for i in range(0, len(activation_HScodeList)):
                        df['HS' + str(i+1)] = [activation_HScodeList[i]]*len(df)
                df['source'] = [activation_source]*len(df)
                print(df)
                df.to_csv(product + '.csv')

            if 'Revocation of Antidumping' in title:
                print(title)
                revocation.append(i)
                revocation_source = i
                revocation_action = 'revocation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                revocation_year = dateString[:4]
                revocation_month = dateString[5:7]
                revocation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n', flags=re.M)
                revocation_FedReg = FedRegFormat.findall(longwebContent)[0]
                HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                revocation_HScodeList = list(HScodeFormate.findall(longwebContent))
                print(len(revocation_HScodeList))
                print(revocation_HScodeList)
    if len(initiation) == 0 or len(activation) == 0:
        print('take a look! we do not have initiation or activation in this product?')
    # if len(activation) > 0:
        # we should only have 1 activation file per product
        # find DOC No., Year, Month, Date, HS1, HS2, HS3, HS4, HS5, HS6, HS7, Product, Country, Exporter, ExpAltNm, Producer, PdAltNm,  ProducerID,  AD_CVD, Dumping Margin, Cash Deposit, Action, Source

    # print("initiation")
    # print(initiation)
    # print("activation")
    # print(activation)
    # print("revocation")
    # print(revocation)
AntiDumping('A-201-842', 'Large Residential Washers')
# AntiDumping('A-201-838', 'Softwood lumber')
# AntiDumping('A-201-840', 'Carbon steel wire rod')

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

