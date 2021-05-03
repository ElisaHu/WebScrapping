import pandas as pd
import urllib.request, urllib.parse
import re

# get numpy array from csv file
my_csv = pd.read_csv('Revocation.csv')
column = my_csv['DOC case No.']
DOCarray = column[1:].values
productColumn = my_csv['Product']
productArray = productColumn[1:].values


def AntiDumping(DOC):
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
        if "initiation-of-antidumping-duty" in i:
            initiation.append(i)
        if "antidumping-duty-orders" in i:
            activation.append(i)
        if "continuation-of-antidumping-duty" in i:
            revocation.append(i)
    print("initiation")
    print(initiation)
    print("activation")
    print(activation)
    print("revocation")
    print(revocation)

AntiDumping('A-583-080')

# def Countervailing(DOC):
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
# for DOC in DOCarray:
#     # get the type: AD/CVD -- first char in a string
#     type = DOC[0]
#     if (type == 'A'):
#         AntiDumping(DOC)
#     elif (type == 'C'):
#         Countervailing(DOC)
#     else:
#         print(DOC)
    # create one csv file for each DOC case
    # csvFile = open('overallData.csv', 'w+')

# --------unworked code------------------------------------------------------
# csvFile = open('Revocation.csv', 'w+')
# content = []
# with open('Revocation.csv', 'rt') as revocation:
#     csv_reader = csv.reader(revocation, delimiter=' ')
#     for row in csv_reader:
#         content.append(list(row[4]))

