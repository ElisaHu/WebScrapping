import csv
import math

import pandas as pd
import urllib.request, urllib.parse
import re
import requests
import numpy as np
import lxml

# get numpy array from csv file
my_csv = pd.read_csv('Sample_overall.csv')
column = my_csv['DOCNo']
DOCarray = column[1:].values
productColumn = my_csv['Product']
productArray = productColumn[1:].values
all_countries = ['PRC','Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

def tryfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def AntiDumping(DOC, product):
    # get the website link, read content from it
    initiation_df = pd.DataFrame()
    activation_df = pd.DataFrame()
    revocation_df = pd.DataFrame()
    HSACTLIST = 0
    HSREVLIST = 0
    HSINILIST = 0
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
    for link in webLinkList:
        productName = product.replace(' ', '-').lower()
        if productName in link or 'notice-of-implementation' in link or 'antidumping' in link:
            longlink = urllib.request.urlopen(link)
            longwebContent = str(longlink.read())
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            print(title)
            if product not in title:
                continue;
            if 'Revocation of Antidumping' in title or 'Revocation of the Antidumping' in title or 'Revocation of Orders' in title:
                if 'Consideration of Revocation' in title:
                    continue
                print('END ' + title)
                print(link)
                revocation.append(link)
                revocation_source = link
                revocation_action = 'revocation'
                countryFormat = re.compile(r'(Revocation.+)', flags=re.M)
                revocation_country = countryFormat.findall(title)[0]
                if len(revocation_country) == 0:
                    revocation_country = title
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in revocation_country:
                        countries.append(c)
                if len(countries) == 0:
                    revocation_country = title
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
                revocation_df['Country'] = countries
                revocation_df['Action'] = [revocation_action]
                revocation_df['Year'] = [revocation_year]
                revocation_df['Month'] = [revocation_month]
                revocation_df['Date'] = [revocation_date]
                revocation_df['FedReg'] = [revocation_FedReg]
                revocation_df['AD/CVD'] = ['AD']
                SOIformat = re.compile(r'Scope of\s(.+?)</h2>(.+?)<h2 id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 5:
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                    # todo: probably fix the order
                    if len(revocation_HScodeList) == 6:
                        for i in range(0, len(revocation_HScodeList) + 1):
                            if i < 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                            if i == 2:
                                revocation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i - 1]]
                    if len(revocation_HScodeList) < 5 or len(revocation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                    HSREVLIST = len(revocation_HScodeList)

                revocation_df['Source'] = [revocation_source]

            if 'Review' in title:
                continue;
            if 'Preliminary' in title:
                continue;
            if 'Corrected Notice' in title:
                continue;
            if product not in title:
                continue;
            if 'Initiation of Antidumping Duty' in title:
                print('INITIATION: ' + title)
                print(link)
                initiation.append(link)
                initiation_source = link
                initiation_action = 'initiation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                initiation_year = dateString[:4]
                initiation_month = dateString[5:7]
                initiation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n', flags=re.M)
                initiation_FedReg = FedRegFormat.findall(longwebContent)[0]
                initiation_petitioners = []
                petitionerFormat1 = re.compile(r'proper\sform\sby\s(.+)\s\(“(?:\w{3}\s)\wetitioner(?:\w)?”\)', flags=re.M)
                if len(petitionerFormat1.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat1.findall(longwebContent)[0])
                petitionerFormat2 = re.compile(r'proper\sform\sby\s(.+?)\s\(&ldquo;(?:\w{3}\s)\wetitioner(?:\w)?&rdquo;\)', flags=re.M)
                if len(petitionerFormat2.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat2.findall(longwebContent)[0])
                petitionerFormat3 = re.compile(r'proper\sform\sby\s(.+?)\s\(collectively, &ldquo;(?:\w{3}\s)\wetitioner(?:\w)?&rdquo;\)',
                                               flags=re.M)
                if len(petitionerFormat3.findall(longwebContent)) != 0:
                    initiation_petitioners = petitionerFormat3.findall(longwebContent)[0].split("and")
                petitionerFormat4 = re.compile(r'on behalf of\s(.+?)\s\(collectively, (?:\w{3}\s)\wetitioner(?:\w)?\)',
                    flags=re.M)
                if len(petitionerFormat4.findall(longwebContent)) != 0:
                    initiation_petitioners = petitionerFormat4.findall(longwebContent)[0].split(",")
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in title:
                        countries.append(c)
                initiation_df['Country'] = countries
                initiation_df['Action'] = [initiation_action] * len(countries)
                initiation_df['Year'] = [initiation_year] * len(countries)
                initiation_df['Month'] = [initiation_month] * len(countries)
                initiation_df['Date'] = [initiation_date] * len(countries)
                initiation_df['FedReg'] = [initiation_FedReg] * len(countries)
                initiation_df['AD/CVD'] = ['AD'] * len(countries)
                for i in range(len(initiation_petitioners)):
                    initiation_df['Petitioner' + str(i + 1)] = initiation_petitioners[i] * len(countries)
                    altnameformat = re.compile(r'\((.+?)\)', flags=re.M)
                    altname = ''
                    if len(altnameformat.findall(initiation_petitioners[i])) > 0:
                        altname = altnameformat.findall(initiation_petitioners[i])[0]
                    initiation_df['Ptner' + str(i + 1) + 'AltNm'] = [altname] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 5:
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                    if len(initiation_HScodeList) == 6:
                        initiation_df['HS' + '3'] = ''
                        for i in range(0, len(initiation_HScodeList) + 1):
                            if i < 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                            if i == 2:
                                initiation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i - 1]] * len(countries)
                    if len(initiation_HScodeList) < 5 or len(initiation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                    HSINILIST = len(initiation_HScodeList)
                initiation_df['Source'] = [initiation_source] * len(countries)

            if 'Antidumping Duty Order' in title and 'Continuation' not in title and 'Pursuant to Court' not in title:
                if 'Correction for' in title:
                    continue
                print('START ' + title)
                print(link)
                activation.append(link)
                activation_source = link
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
                html = requests.get(link).content
                df_list = pd.read_html(html)
                activation_df = pd.DataFrame(df_list[-1])
                if len(activation_df.columns.tolist()) == len(df_list[-2].columns.tolist()):
                    # add country
                    countryFormat = re.compile(r'<p class="title">.+?From(.+?)</p>', flags=re.M)
                    activation_countryFormat = countryFormat.findall(longwebContent)
                    if len(activation_countryFormat) > 0:
                        for i in range(len(activation_countryFormat)):
                            if 'PRC' in activation_countryFormat[i]:
                                activation_countryFormat[i] = 'China'
                            activation_countryFormat[i] = activation_countryFormat[i].replace(" ", "")
                    else:
                        columnnamelist = []
                        columnnamelist.append(df_list[-2].columns.tolist()[0])
                        columnnamelist.append(df_list[-1].columns.tolist()[0])
                        for c in all_countries:
                            if c in df_list[-2].columns.tolist()[0]:
                                if c == 'PRC':
                                    c = 'China'
                                activation_countryFormat.append(c)
                        for c in all_countries:
                            if c in df_list[-1].columns.tolist()[0]:
                                if c == 'PRC':
                                    c = 'China'
                                activation_countryFormat.append(c)

                    df_list[-2]['Country'] = [activation_countryFormat[0]] * len(df_list[-2])
                    activation_df['Country'] = [activation_countryFormat[1]] * len(activation_df)

                    activation_df = activation_df.append(df_list[-2], ignore_index=True)

                # fill first column value
                last = ''
                firstcolumn = []
                firstcolumnname = activation_df.columns.tolist()[0]
                lastcolumnname = activation_df.columns.tolist()[-1]
                activation_df[lastcolumnname] = activation_df[lastcolumnname].astype(float, errors='ignore')
                if tryfloat(activation_df[lastcolumnname][0]) and tryfloat(activation_df[lastcolumnname][1]):
                    activation_df = activation_df[activation_df[lastcolumnname].apply(lambda x: tryfloat(x))]
                    activation_df = activation_df.reset_index(drop=True)

                if firstcolumnname == 'Country' or firstcolumnname == 'Countries':
                    secondcolumnname = activation_df.columns.tolist()[1]
                    activation_df = activation_df.rename({secondcolumnname: 'Exporter'}, axis=1)
                else:
                    activation_df = activation_df.rename({firstcolumnname: 'Exporter'}, axis=1)
                    firstcolumnname = 'Exporter'

                len_of_act = len(activation_df)
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
                            countries = [c] * len_of_act
                    activation_df['Country'] = countries

                if 'Producer' not in activation_df.columns.tolist():
                    activation_df['Producer'] = activation_df['Exporter'].copy()

                activation_df['Year'] = [activation_year] * len_of_act
                activation_df['Month'] = [activation_month] * len_of_act
                activation_df['Date'] = [activation_date] * len_of_act
                activation_df['FedReg'] = [activation_FedReg] * len_of_act
                activation_df['AD/CVD'] = ['AD'] * len_of_act
                activation_df['Action'] = [activation_action] * len_of_act

                SOIformat = re.compile(r'Scope of\s(.+?)</h\d{1}>(.+?)<h\d{1} id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 5:
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                    if len(activation_HScodeList) == 6:
                        activation_df['HS' + '3'] = ''
                        for i in range(0, len(activation_HScodeList) + 1):
                            if i < 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                            if i == 2:
                                activation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i - 1]] * len_of_act
                    if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                    HSACTLIST = len(activation_HScodeList)
                activation_df['Source'] = [activation_source] * len_of_act


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
        combine_act_rev_list = ["FedReg", "Country", "Exporter", "Producer", "Year",
                                "Month", "Date", "AD/CVD", "Action", "Source"]
        # if "Dumping margin" in revocation_df:
        #     combine_act_rev_list.append("Dumping margin")
        for eachHS in range(min(HSREVLIST, HSACTLIST)):
            combine_act_rev_list.append("HS" + str(eachHS + 1))
        if len(initiation) != 0:
            for i in Petitioner_column:
                combine_act_rev_list.append(i)
        combine_act_rev = revocation_df.merge(activation_df, on=list(combine_act_rev_list), how='outer')
    else:
        HSREVLIST = HSACTLIST
        combine_act_rev = activation_df
    if len(initiation) == 0:
        combine_act_rev = combine_act_rev.sort_values('Year')
        cols = list(combine_act_rev.columns.values)
        cols.pop(cols.index('Source'))
        combine_int_rest = combine_act_rev[cols + ['Source']]
        combine_act_rev.to_csv(product + '_AD.csv', index=False)
        return

    combine_column = ["Country", "FedReg", "Year", "Month", "Date", "AD/CVD", "Action", "Exporter", "Producer", "Source"]
    for i in Petitioner_column:
        combine_column.append(i)
    for eachHS in range(min(HSINILIST, HSREVLIST, HSACTLIST)):
        combine_column.append("HS" + str(eachHS + 1))
    combine_int_rest = initiation_df.merge(combine_act_rev, on=list(combine_column), how='outer')
    combine_int_rest = combine_int_rest.sort_values('Year')
    cols = list(combine_int_rest.columns.values)
    cols.pop(cols.index('Source'))
    combine_int_rest = combine_int_rest[cols + ['Source']]
    combine_int_rest.to_csv(product + '_AD.csv', index=False)

# AntiDumping('A-580-855', 'Diamond Sawblades')  # have all 3 phase, 2 table in action
# AntiDumping('A-201-842', 'Large Residential Washers')  # first example
# AntiDumping('A-580-850', 'Polyvinyl Alcohol')
# AntiDumping('A-570-979', 'Crystalline Silicon Photovoltaic Cells')
# AntiDumping('A-201-828', 'Welded Large Diameter Line Pipes') # cannot do this, missing DOC number
# AntiDumping('A-437-804', 'Sulfanilic Acid') # irregular format of the table, revocation with FA
AntiDumping('A-307-820', 'Silicomanganese')
# AntiDumping('A-570-890', 'Wooden Bedroom Furniture')

def Countervailing(DOC, product):
    # get the website link, read content from it
    initiation_df = pd.DataFrame()
    activation_df = pd.DataFrame()
    revocation_df = pd.DataFrame()
    HSACTLIST = 0
    HSREVLIST = 0
    HSINILIST = 0
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
    for link in webLinkList:
        productName = product.replace(' ', '-').lower()
        if productName in link or 'notice-of-implementation' in link or 'countervailing' in link:
            longlink = urllib.request.urlopen(link)
            longwebContent = str(longlink.read())
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            print(title)
            if product not in title:
                continue;
            if 'Pursuant to Court Decision' in title:
                continue
            if ('Revocation of' in title and 'Countervailing' in title) or 'Revocation of Orders' in title:
                if 'Consideration of Revocation' in title:
                    continue
                if 'Countervailing Duty Orders' not in title:
                    continue
                print('END ' + title)
                print(link)
                revocation.append(link)
                revocation_source = link
                revocation_action = 'revocation'
                countryFormat = re.compile(r'(Revocation.+)', flags=re.M)
                revocation_country = countryFormat.findall(title)[0]
                if len(revocation_country) == 0:
                    revocation_country = title
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in revocation_country:
                        countries.append(c)
                if len(countries) == 0:
                    revocation_country = title
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
                revocation_df['Country'] = countries
                revocation_df['Action'] = [revocation_action]
                revocation_df['Year'] = [revocation_year]
                revocation_df['Month'] = [revocation_month]
                revocation_df['Date'] = [revocation_date]
                revocation_df['FedReg'] = [revocation_FedReg]
                revocation_df['AD/CVD'] = ['CVD']
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 5:
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                    # todo: probably fix the order
                    if len(revocation_HScodeList) == 6:
                        for i in range(0, len(revocation_HScodeList) + 1):
                            if i < 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                            if i == 2:
                                revocation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i - 1]]
                    if len(revocation_HScodeList) < 5 or len(revocation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]]
                    HSREVLIST = len(revocation_HScodeList)

                revocation_df['Source'] = [revocation_source]

            if 'Review' in title:
                continue;
            if 'Preliminary' in title:
                continue;
            if 'Corrected Notice' in title:
                continue;
            if product not in title:
                continue;
            if 'Initiation of Countervailing Duty' in title or ('Initiation of' in title and 'Countervailing' in title):
                if 'Correction to' in title or 'Anti-Circumvention Inquiries' in title:
                    continue
                print('INITIATION: ' + title)
                print(link)
                initiation.append(link)
                initiation_source = link
                initiation_action = 'initiation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                initiation_year = dateString[:4]
                initiation_month = dateString[5:7]
                initiation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{4,5})\\n', flags=re.M)
                initiation_FedReg = FedRegFormat.findall(longwebContent)[0]
                initiation_petitioners = []
                petitionerFormat1 = re.compile(r'proper\sform\sby\s(.+)\s\(“(?:\w{3}\s)\wetitioner(?:\w)?”\)', flags=re.M)
                if len(petitionerFormat1.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat1.findall(longwebContent)[0])
                petitionerFormat2 = re.compile(r'proper\sform\sby\s(.+?)\s\(&ldquo;(?:\w{3}\s)\wetitioner(?:\w)?&rdquo;\)', flags=re.M)
                if len(petitionerFormat2.findall(longwebContent)) != 0:
                    initiation_petitioners.append(petitionerFormat2.findall(longwebContent)[0])
                petitionerFormat3 = re.compile(r'proper\sform\sby\s(.+?)\s\(collectively, &ldquo;(?:\w{3}\s)\wetitioner(?:\w)?&rdquo;\)',
                                               flags=re.M)
                if len(petitionerFormat3.findall(longwebContent)) != 0:
                    initiation_petitioners = petitionerFormat3.findall(longwebContent)[0].split("and")
                petitionerFormat4 = re.compile(r'on behalf of\s(.+?)\s\(collectively, (?:\w{3}\s)\wetitioner(?:\w)?\)',
                    flags=re.M)
                if len(petitionerFormat4.findall(longwebContent)) != 0:
                    initiation_petitioners = petitionerFormat4.findall(longwebContent)[0].split(",")
                countries = []
                for c in all_countries:
                    # check if Country is in TXT
                    if c in title:
                        countries.append(c)
                initiation_df['Country'] = countries
                initiation_df['Action'] = [initiation_action] * len(countries)
                initiation_df['Year'] = [initiation_year] * len(countries)
                initiation_df['Month'] = [initiation_month] * len(countries)
                initiation_df['Date'] = [initiation_date] * len(countries)
                initiation_df['FedReg'] = [initiation_FedReg] * len(countries)
                initiation_df['AD/CVD'] = ['CVD'] * len(countries)
                for i in range(len(initiation_petitioners)):
                    # companyformat = re.compile(r'([A-Z])', flags=re.M)
                    # company = companyformat.findall(initiation_petitioners[i])[1]
                    initiation_df['Petitioner' + str(i + 1)] = initiation_petitioners[i] * len(countries)
                    altnameformat = re.compile(r'\((.+?)\)', flags=re.M)
                    altname = ''
                    if len(altnameformat.findall(initiation_petitioners[i])) > 0:
                        altname = altnameformat.findall(initiation_petitioners[i])[0]
                    initiation_df['Ptner' + str(i + 1) + 'AltNm'] = [altname] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 5:
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                    if len(initiation_HScodeList) == 6:
                        initiation_df['HS' + '3'] = ''
                        for i in range(0, len(initiation_HScodeList) + 1):
                            if i < 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                            if i == 2:
                                initiation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i - 1]] * len(countries)
                    if len(initiation_HScodeList) < 5 or len(initiation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]] * len(countries)
                    HSINILIST = len(initiation_HScodeList)
                initiation_df['Source'] = [initiation_source] * len(countries)

            if 'Affirmative Final Determination' in title:
                continue
            if 'Countervailing Duty Order' in title and 'Continuation' not in title and 'Pursuant to Court' not in title:
                if 'Correction for' in title or 'Initiation' in title:
                    continue
                print('START ' + title)
                print(link)
                activation.append(link)
                activation_source = link
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
                html = requests.get(link).content
                df_list = pd.read_html(html)
                activation_df = pd.DataFrame(df_list[-1])
                if len(activation_df.columns.tolist()) == len(df_list[-2].columns.tolist()):
                    # add country
                    countryFormat = re.compile(r'<p class="title">.+?From(.+?)</p>', flags=re.M)
                    activation_countryFormat = countryFormat.findall(longwebContent)
                    if len(activation_countryFormat) > 0:
                        for i in range(len(activation_countryFormat)):
                            if 'PRC' in activation_countryFormat[i]:
                                activation_countryFormat[i] = 'China'
                            activation_countryFormat[i] = activation_countryFormat[i].replace(" ", "")
                    else:
                        columnnamelist = []
                        columnnamelist.append(df_list[-2].columns.tolist()[0])
                        columnnamelist.append(df_list[-1].columns.tolist()[0])
                        for c in all_countries:
                            if c in df_list[-2].columns.tolist()[0]:
                                if c == 'PRC':
                                    c = 'China'
                                activation_countryFormat.append(c)
                        for c in all_countries:
                            if c in df_list[-1].columns.tolist()[0]:
                                if c == 'PRC':
                                    c = 'China'
                                activation_countryFormat.append(c)

                    df_list[-2]['Country'] = [activation_countryFormat[0]] * len(df_list[-2])
                    activation_df['Country'] = [activation_countryFormat[1]] * len(activation_df)

                    activation_df = activation_df.append(df_list[-2], ignore_index=True)


            # fill first column value
                last = ''
                firstcolumn = []
                firstcolumnname = activation_df.columns.tolist()[0]
                lastcolumnname = activation_df.columns.tolist()[-1]
                activation_df[lastcolumnname] = activation_df[lastcolumnname].astype(float, errors='ignore')
                if tryfloat(activation_df[lastcolumnname][0]):
                    activation_df = activation_df[activation_df[lastcolumnname].apply(lambda x: tryfloat(x))]
                    activation_df = activation_df.reset_index(drop=True)

                if firstcolumnname == 'Country' or firstcolumnname == 'Countries':
                    secondcolumnname = activation_df.columns.tolist()[1]
                    activation_df = activation_df.rename({secondcolumnname: 'Exporter'}, axis=1)
                else:
                    activation_df = activation_df.rename({firstcolumnname: 'Exporter'}, axis=1)
                    firstcolumnname = 'Exporter'

                len_of_act = len(activation_df)
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
                            countries = [c] * len_of_act
                    activation_df['Country'] = countries

                if 'Producer' not in activation_df.columns.tolist():
                    activation_df['Producer'] = activation_df['Exporter'].copy()

                activation_df['Year'] = [activation_year] * len_of_act
                activation_df['Month'] = [activation_month] * len_of_act
                activation_df['Date'] = [activation_date] * len_of_act
                activation_df['FedReg'] = [activation_FedReg] * len_of_act
                activation_df['AD/CVD'] = ['CVD'] * len_of_act
                activation_df['Action'] = [activation_action] * len_of_act
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d{1}>(.+?)<h\d{1} id=', flags=re.M)
                SOI = SOIformat.findall(longwebContent)[1][1]
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 5:
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                    if len(activation_HScodeList) == 6:
                        activation_df['HS' + '3'] = ''
                        for i in range(0, len(activation_HScodeList) + 1):
                            if i < 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                            if i == 2:
                                activation_df['HS' + str(i + 1)] = ''
                            if i > 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i - 1]] * len_of_act
                    if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:
                        print('irregular HScode')
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]] * len_of_act
                    HSACTLIST = len(activation_HScodeList)
                activation_df['Source'] = [activation_source] * len_of_act


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
        combine_act_rev_list = ["FedReg", "Country", "Exporter", "Producer", "Year",
                                "Month", "Date", "AD/CVD", "Action", "Source"]
        # if "Dumping margin" in revocation_df:
        #     combine_act_rev_list.append("Dumping margin")
        for eachHS in range(min(HSREVLIST, HSACTLIST)):
            combine_act_rev_list.append("HS" + str(eachHS + 1))
        if len(initiation) != 0:
            for i in Petitioner_column:
                combine_act_rev_list.append(i)
        combine_act_rev = revocation_df.merge(activation_df, on=list(combine_act_rev_list), how='outer')
    else:
        HSREVLIST = HSACTLIST
        combine_act_rev = activation_df
    if len(initiation) == 0:
        combine_act_rev = combine_act_rev.sort_values('Year')
        cols = list(combine_act_rev.columns.values)
        cols.pop(cols.index('Source'))
        combine_int_rest = combine_act_rev[cols + ['Source']]
        combine_act_rev.to_csv(product + '_AD.csv', index=False)
        return

    combine_column = ["Country", "FedReg", "Year", "Month", "Date", "AD/CVD", "Action", "Exporter", "Producer",
                      "Source"]
    for i in Petitioner_column:
        combine_column.append(i)
    for eachHS in range(min(HSINILIST, HSREVLIST, HSACTLIST)):
        combine_column.append("HS" + str(eachHS + 1))
    combine_int_rest = initiation_df.merge(combine_act_rev, on=list(combine_column), how='outer')
    combine_int_rest = combine_int_rest.sort_values('Year')
    cols = list(combine_int_rest.columns.values)
    cols.pop(cols.index('Source'))
    combine_int_rest = combine_int_rest[cols + ['Source']]
    combine_int_rest.to_csv(product + '_CVD.csv', index=False)


# Countervailing('C-580-869', 'Large Residential Washers')
# Countervailing('C-570-025', 'Polyethylene Terephthalate Resin')
# Countervailing('C-122-858', 'Softwood Lumber Products')
# Countervailing('C-570-030', 'Cold-Rolled Steel Flat Products')
# Countervailing('C-533-872', 'Finished Carbon Steel Flanges')
# Countervailing('C-570-966', 'Drill Pipe')
# Countervailing('C-570-948', 'Steel Grating')
# Countervailing('C-570-953', 'Narrow Woven Ribbons With Woven Selvedge')
# Countervailing('C-489-825', 'Heavy Walled Rectangular Welded Carbon Steel Pipes and Tubes')
# iterating over each DOC Number

# for index in range(0, len(DOCarray)):
#     # get the type: AD/CVD -- first char in a string
#     type = DOCarray[index][0]
#     if (type == 'A'):
#         AntiDumping(DOCarray[index], productArray[index])
#     elif (type == 'C'):
#         Countervailing(DOCarray[index], productArray[index])
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

