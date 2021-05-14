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
all_countries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

def AntiDumping(DOC, product):
    # get the website link, read content from it
    initiation_df = pd.DataFrame()
    activation_df = pd.DataFrame()
    revocation_df = pd.DataFrame()
    url = 'https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=' + DOC
    response = urllib.request.urlopen(url)
    webContent = str(response.read())
    for pageNum in range(2, 20):
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
    # print(len(webLinkList))
    initiation = []
    activation = []
    revocation = []
    for i in webLinkList:
        productName = product.replace(' ', '-').lower()
        if productName in i:
            longlink = urllib.request.urlopen(i)
            longwebContent = str(longlink.read())
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            print(title)
            if 'Review' in title:
                continue;
            if 'Preliminary' in title:
                continue;
            if 'Notice' in title:
                continue;
            if product not in title:
                continue;
            if 'Initiation of Antidumping Duty' in title:
                print('initiation: ' + title)
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
                petitionerFormat1 = re.compile(r'proper\sform\sby\s(.+)\s\(“the petitioner”\)',flags=re.M)
                if len(petitionerFormat1.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat1.findall(longwebContent)[0])
                petitionerFormat2 = re.compile(r'proper\sform\sby\s(.+?)\s\(&ldquo;Petitioner&rdquo;\)', flags=re.M)
                if len(petitionerFormat2.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat2.findall(longwebContent)[0])
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in title:
                        countries.append(c)
                initiation_df['Country'] = countries
                initiation_df['Action'] = [initiation_action]*len(countries)
                initiation_df['Year'] = [initiation_year]*len(countries)
                initiation_df['Month'] = [initiation_month]*len(countries)
                initiation_df['Date'] = [initiation_date]*len(countries)
                initiation_df['FedReg'] = [initiation_FedReg]*len(countries)
                initiation_df['AD/CVD'] = ['AD']*len(countries)
                for i in range(len(initiation_petitioners)):
                    initiation_df['Petitioner' + str(i+1)] = initiation_petitioners[i]*len(countries)
                    initiation_df['Ptner' + str(i +1) + 'AltNm'] = ['']*len(countries)
                initiation_df['Source'] = [initiation_source]*len(countries)

            if 'Revocation of Antidumping' in title or 'Revocation of the Antidumping' in title:
                print('end' + title)
                revocation.append(i)
                revocation_source = i
                revocation_action = 'revocation'
                countryFormat = re.compile(r'(Revocation.+)', flags=re.M)
                revocation_country = countryFormat.findall(title)[0]
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in revocation_country:
                        countries.append(c)
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                revocation_year = dateString[:4]
                revocation_month = dateString[5:7]
                revocation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n', flags=re.M)
                revocation_FedReg = FedRegFormat.findall(longwebContent)[0]
                HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                revocation_HScodeList = list(HScodeFormate.findall(longwebContent))
                revocation_df['Country'] = countries
                revocation_df['Action'] = [revocation_action]
                revocation_df['Year'] = [revocation_year]
                revocation_df['Month'] = [revocation_month]
                revocation_df['Date'] = [revocation_date]
                revocation_df['FedReg'] = [revocation_FedReg]
                revocation_df['AD/CVD'] = ['AD']
                if len(revocation_HScodeList) == 5:
                    for i in range(0, len(revocation_HScodeList)):
                        revocation_df['HS' + str(i+1)] = [revocation_HScodeList[i]]
                # todo: probably fix the order
                if len(revocation_HScodeList) == 6:
                    for i in range(0, len(revocation_HScodeList)+1):
                        if i < 2:
                            revocation_df['HS' + str(i+1)] = [revocation_HScodeList[i]]
                        if i == 2:
                            revocation_df['HS' + str(i + 1)] = ''
                        if i > 2:
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i-1]]
                if len(revocation_HScodeList) < 5 or len(revocation_HScodeList) > 6:
                    print('irregular HScode')
                    for i in range(0, len(revocation_HScodeList)):
                        revocation_df['HS' + str(i+1)] = [revocation_HScodeList[i]]

                revocation_df['Source'] = [revocation_source]
                revocation_df.to_csv(product + '_revocation.csv')

            if 'Antidumping Duty Order' in title and 'Continuation' not in title:
                print('start ' + title)
                print(i)
                activation.append(i)
                activation_source = i
                activation_action = 'activation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})',
                                        flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                activation_year = dateString[:4]
                activation_month = dateString[5:7]
                activation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{3,5})\\n',
                                          flags=re.M)
                activation_FedReg = FedRegFormat.findall(longwebContent)[0]
                html = requests.get(i).content
                df_list = pd.read_html(html)
                activation_df = pd.DataFrame(df_list[-1])
                len_of_act = len(activation_df)
                # fill first column value
                last = ''
                firstcolumn = []
                firstcolumnname = activation_df.columns.tolist()[0]
                for i in range(len_of_act):
                    curr = activation_df[firstcolumnname][i]
                    if isinstance(curr, str):
                        last = curr
                        firstcolumn.append(curr)
                    else:
                        firstcolumn.append(last)
                activation_df[firstcolumnname] = firstcolumn
                if 'Country' not in activation_df.columns.tolist():
                    countries = []
                    for c in all_countries:
                        # check if Country is in TXT
                        if c in title:
                            countries = [c]*len_of_act
                # if activation_df.columns.tolist().
                if 'Producer' not in activation_df.columns.tolist():
                    activation_df['Producer'] = activation_df['Exporter'].copy()

                activation_df['Country'] = countries
                activation_df['Year'] = [activation_year]*len_of_act
                activation_df['Month'] = [activation_month]*len_of_act
                activation_df['Date'] = [activation_date]*len_of_act
                activation_df = activation_df.rename({'Manufacturer/Exporter': 'Exporter'}, axis=1)
                activation_df['FedReg'] = [activation_FedReg]*len_of_act
                activation_df['AD/CVD'] = ['AD']*len_of_act
                activation_df['Action'] = [activation_action]*len_of_act

                HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                activation_HScodeList = list(HScodeFormate.findall(longwebContent))
                if len(activation_HScodeList) == 5:
                    for i in range(0, len(activation_HScodeList)):
                        activation_df['HS' + str(i+1)] = [activation_HScodeList[i]]*len_of_act
                if len(activation_HScodeList) == 6:
                    activation_df['HS' + '3'] = ''
                    for i in range(0, len(activation_HScodeList)+1):
                        if i < 2:
                            activation_df['HS' + str(i+1)] = [activation_HScodeList[i]]*len_of_act
                        if i == 2:
                            activation_df['HS' + str(i + 1)] = ''
                        if i > 2:
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i-1]]*len_of_act
                if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:
                    print('irregular HScode')
                    for i in range(0, len(activation_HScodeList)):
                        activation_df['HS' + str(i+1)] = [activation_HScodeList[i]]*len_of_act
                activation_df['Source'] = [activation_source]*len_of_act
                activation_df.to_csv(product + '_activation.csv')


    # special for initiation: petitioners
    # special for activation: "Dumping margin","Cash deposit (%)", "Exporter"
    if len(initiation) == 0 or len(activation) == 0:
        print('take a look! we do not have initiation or activation in this product?')
    if len(initiation) != 0:
        Petitioner_column = [col for col in initiation_df.columns if 'Petitioner' in col or 'Ptner' in col]
        Petitioner_column.append("Country")
        initiation_df_subset = initiation_df[Petitioner_column]
        if not activation_df.empty:
            activation_df = activation_df.merge(initiation_df_subset, on=["Country"])
        if not revocation_df.empty:
            revocation_df = revocation_df.merge(initiation_df_subset, on=["Country"])
    if len(activation) != 0:
        # activation_df_subset = activation_df[["Country", "Dumping margin", "Cash deposit (%)", "Exporter"]]
        activation_df_subset = activation_df[["Country", "Exporter", "Producer"]]
        if not initiation_df.empty:
            initiation_df = activation_df_subset.merge(initiation_df, on=["Country"])
        if not revocation_df.empty:
            revocation_df = activation_df_subset.merge(revocation_df, on=["Country"])

    if len(revocation) != 0:
        combine_act_rev = revocation_df.merge(activation_df, on=["FedReg", "Country", "Dumping margin", "Exporter", "Producer"
                                                 "HS1", "HS2", "HS3", "HS4", "HS5", "Year", "Month", "Date", "AD/CVD",
                                                 "Action", "Source"], how='outer')
    else:
        combine_act_rev = activation_df
    if len(initiation) == 0:
        combine_act_rev.to_csv(product + '.csv', index=False)
        return

    combine_column = ["Country", "FedReg", "Year", "Month", "Date", "AD/CVD", "Action", "Exporter", "Producer", "Source"]
    for i in Petitioner_column:
        combine_column.append(i)
    combine_int_rest = initiation_df.merge(combine_act_rev, on=list(combine_column), how='outer')
    combine_int_rest = combine_int_rest.sort_values('Year')
    combine_int_rest.to_csv(product + '.csv', index=False)

# AntiDumping('A-201-842', 'Large Residential Washers')
AntiDumping('A-580-850', 'Polyvinyl Alcohol')
# AntiDumping('A-570-979', 'Crystalline Silicon Photovoltaic Cells')

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

