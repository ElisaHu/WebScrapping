import pandas as pd
import urllib.request, urllib.parse
from urllib.request import Request, urlopen
import re
import requests

# get numpy array from csv file
emptytxt = open("emptyfile.txt", "a")
tooOldfile = open('tooOldfile.txt', 'a')
# noinittxt = open("noinitiation.txt", "a")
# noacttxt = open("noactivation.txt", "a")
# norevocatiotxt = open("norevocation.txt", "a")
# throwerrortxt = open("throwerror.txt", "a")
# my_csv = pd.read_csv('revocationOverall.csv')
my_csv = pd.read_csv('CaseList - No Error.csv')
column = my_csv['DOC case No.']
DOCarray = column[0:].values
productColumn = my_csv['Product']
productArray = productColumn[0:].values
all_countries = ['Afghanistan', 'Aland IslaTaiwannds', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China',  'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'PRC', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom','UK', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

def tryfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def startprint(x):
    if 'Start Print' in x or 'Start Printed' in x:
        return False
    else:
        return True

def iscountry(x):
    if x in all_countries:
        return False
    else:
        return True

def AntiDumping(DOC, product):
    initiation_df = pd.DataFrame()
    activation_df = pd.DataFrame()
    revocation_df = pd.DataFrame()
    HSACTLIST = 0
    HSREVLIST = 0
    HSINILIST = 0
    url = 'https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=' + DOC
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # webpage = urlopen(req).read()
    # response = urllib.request.urlopen(url)
    webContent = str(urlopen(req).read())
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
    webLinkFormat = re.compile(r'"(https://www.federalregister.gov/documents/\d+.+?)"', flags=re.M)
    webLinkList = webLinkFormat.findall(webContent)
    initiation = []
    activation = []
    revocation = []
    productName = product.replace(' ', '-').lower()
    productName = productName.replace('&', 'and')
    productName = productName.replace(',', '')
    for link in webLinkList:
        if productName in link or 'notice-of-implementation' in link or 'antidumping' in link:
            longlink = urllib.request.urlopen(link)
            longwebContent = str(longlink.read())
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            oldPattern = re.compile(r'The full text of this document is', flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            oldformat = oldPattern.findall(longwebContent)
            if 'Pursuant to Court Decision' in title or 'Notice of Correction' in title or 'Amended Final Results of Full Sunset Review'  in title or 'Antidumping or Countervailing Duty Order, Finding, or Suspended Investigation; Opportunity to Request Administrative Review' in title:
                continue
            if product not in title:
                continue
            print(title)
            if 'Revocation of Antidumping' in title or 'Revocation of the Antidumping' in title or 'Revocation of Orders' in title:
                if 'Consideration of Revocation' in title or 'Partial Revocation' in title:
                    continue
                print('END ' + title)
                print(link)
                if len(oldformat) > 0:
                    print('Revocation File is too old')
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    continue
                revocation.append(link)
                revocation_source = link
                revocation_action = 'revocation'
                countryFormat = re.compile(r'(Revocation.+)', flags=re.M)
                revocation_country = countryFormat.findall(title)[0]
                if len(revocation_country) == 0:
                    revocation_country = title
                countries = []
                for c in all_countries:
                    if c in revocation_country:
                        countries.append(c)
                if len(countries) == 0:
                    revocation_country = title
                    for c in all_countries:
                        if c in revocation_country:
                            countries.append(c)
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                revocation_year = dateString[:4]
                revocation_month = dateString[5:7]
                revocation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{3,5})\\n', flags=re.M)
                revocation_FedReg = FedRegFormat.findall(longwebContent)[0]
                revocation_df['Country'] = countries
                revocation_df['Action'] = [revocation_action] * len(countries)
                revocation_df['Year'] = [revocation_year] * len(countries)
                revocation_df['Month'] = [revocation_month] * len(countries)
                revocation_df['Date'] = [revocation_date] * len(countries)
                revocation_df['FedReg'] = [revocation_FedReg] * len(countries)
                revocation_df['AD/CVD'] = ['AD'] * len(countries)
                revocation_df['DOC'] = [DOC] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 5:
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                    # todo: probably fix the order
                    if len(revocation_HScodeList) == 6:
                        for i in range(0, len(revocation_HScodeList) + 1):
                            if i < 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                            if i == 2:
                                revocation_df['HS' + str(i + 1)] = [''] * len(countries)
                            if i > 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i - 1]] * len(countries)
                    if len(revocation_HScodeList) < 5 or len(revocation_HScodeList) > 6:
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                    HSREVLIST = len(revocation_HScodeList)

                revocation_df['Source'] = [revocation_source] * len(countries)
                continue

            if 'Preliminary' in title or 'New Shipper Review' in title or 'Corrected Notice' in title or 'Changed Circumstances Review' in title or 'Changed-Circumstances Review' in title or 'Final Result' in title or 'Amendment to' in title or 'Notice of Reinstatement' in title:
                continue
            if 'Initiation of Antidumping Duty' in title or 'Initiation of Less-Than-Fair-Value' in title:
                if 'Revocation' in title or 'Notice of Amended' in title:
                    continue
                print('INITIATION: ' + title)
                print(link)
                if len(oldformat) > 0:
                    print('Initiation File is too old')
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    continue
                initiation.append(link)
                initiation_source = link
                initiation_action = 'initiation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                initiation_year = dateString[:4]
                initiation_month = dateString[5:7]
                initiation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{3,5})\\n', flags=re.M)
                initiation_FedReg = FedRegFormat.findall(longwebContent)[0]
                initiation_petitioners = []
                petitionerFormat1 = re.compile(r'proper\sform\s(?:by)?(?:on behalf of)?(.+)\((?:collectively,?\s)?(?:“)?(?:\w{3}\s)?(?:“)?\wetitioner(?:\w)?(?:")?\)', flags=re.M)
                if len(petitionerFormat1.findall(longwebContent)) != 0:
                    if ',' in petitionerFormat1.findall(longwebContent)[0]:
                        initiation_petitioners = petitionerFormat1.findall(longwebContent)[0].split(",")
                    else:
                        initiation_petitioners = petitionerFormat1.findall(longwebContent)[0].split("and")
                petitionerFormat2 = re.compile(r'proper\sform\s(?:by)?(?:on behalf of)?\s(.+?)\((?:collectively,?\s)?(?:&ldquo;)?(?:\w{3}\s)?(?:&ldquo;)?\wetitioner(?:\w)?&rdquo;\)',
                                               flags=re.M)
                if len(petitionerFormat2.findall(longwebContent)) != 0:
                    if ',' in petitionerFormat2.findall(longwebContent)[0]:
                        initiation_petitioners = petitionerFormat2.findall(longwebContent)[0].split(",")
                    else:
                        initiation_petitioners = petitionerFormat2.findall(longwebContent)[0].split("and")
                countries = []
                for c in all_countries:
                    if c in title:
                        countries.append(c)
                initiation_df['Country'] = countries
                initiation_df['Action'] = [initiation_action] * len(countries)
                initiation_df['Year'] = [initiation_year] * len(countries)
                initiation_df['Month'] = [initiation_month] * len(countries)
                initiation_df['Date'] = [initiation_date] * len(countries)
                initiation_df['FedReg'] = [initiation_FedReg] * len(countries)
                initiation_df['AD/CVD'] = ['AD'] * len(countries)
                if len(initiation_petitioners) == 0:
                    initiation_df['no petitioner'] = ['1']*len(countries)
                else:
                    for i in range(len(initiation_petitioners)):
                        initiation_df['Petitioner' + str(i + 1)] = [initiation_petitioners[i]] * len(countries)
                        altnameformat = re.compile(r'\((.+?)\)', flags=re.M)
                        altname = ''
                        if len(altnameformat.findall(initiation_petitioners[i])) > 0:
                            altname = altnameformat.findall(initiation_petitioners[i])[0]
                        initiation_df['Ptner' + str(i + 1) + 'AltNm'] = [altname] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 5:
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                    # todo: probably fix the order
                    if len(initiation_HScodeList) == 6:
                        for i in range(0, len(initiation_HScodeList) + 1):
                            if i < 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                            if i == 2:
                                initiation_df['HS' + str(i + 1)] = [''] * len(countries)
                            if i > 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i - 1]]* len(countries)
                    if len(initiation_HScodeList) < 5 or len(initiation_HScodeList) > 6:

                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                    HSINILIST = len(initiation_HScodeList)
                initiation_df['DOC'] = [DOC] * len(countries)
                initiation_df['Source'] = [initiation_source] * len(countries)
                continue

            if 'Correction for' in title or 'Correction to' in title or 'Circumvention' in title or 'Notice of Amended' in title or 'Notice of Rescission' in title or 'Continuation' in title or 'Negative Final Determination' in title or 'Pursuant to Court' in title or 'Revocation' in title or 'Initiation' in title or 'Amended Antidumping Duty Orders' in title:
                continue

            if 'Antidumping Duty Order' in title or 'Antidumping Duty and Countervailing Duty Orders' in title:
                print('START ' + title)
                print(link)

                if len(oldformat) > 0:
                    print('activation File is too old')
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    continue
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
                counttables = 1
                if len(activation_df.columns.tolist()) == len(df_list[-2].columns.tolist()) and activation_df.columns[-1] == df_list[-2].columns[-1]:
                    counttables = 2
                    if len(df_list[-3].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-3].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 3
                    if len(df_list[-4].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-4].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 4
                    if len(df_list[-5].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-5].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 5
                    if len(df_list[-6].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-6].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 6
                    countryFormatInTitle = re.compile(r'From(.+)', flags=re.M)
                    activation_countryFormat_in_title = countryFormatInTitle.findall(title)
                    columnnamelist = []
                    # if len(activation_countryFormat) > 0:
                    #     for i in range(len(activation_countryFormat)):
                    #         if 'PRC' in activation_countryFormat[i]:
                    #             activation_countryFormat[i] = 'China'
                    #         activation_countryFormat[i] = activation_countryFormat[i].replace(" ", "")
                    if len(activation_countryFormat_in_title) > 0:
                        for c in all_countries:
                            if c in activation_countryFormat_in_title[0]:
                                columnnamelist.append(c)
                    # else:
                    #     if counttables == 3:
                    #         columnnamelist.append(df_list[-3].columns.tolist()[0])
                    #     columnnamelist.append(df_list[-2].columns.tolist()[0])
                    #     columnnamelist.append(df_list[-1].columns.tolist()[0])
                    #
                    #     if counttables == 3:
                    #         for c in all_countries:
                    #             if c in df_list[-2].columns.tolist()[0]:
                    #                 if c == 'PRC':
                    #                     c = 'China'
                    #                 activation_countryFormat.append(c)
                    #
                    #     for c in all_countries:
                    #         if c in df_list[-2].columns.tolist()[0]:
                    #             if c == 'PRC':
                    #                 c = 'China'
                    #             activation_countryFormat.append(c)
                    #     for c in all_countries:
                    #         if c in df_list[-1].columns.tolist()[0]:
                    #             if c == 'PRC':
                    #                 c = 'China'
                    #             activation_countryFormat.append(c)
                    for eachtable in range(counttables):
                        if eachtable == 1:
                            activation_df['Country'] = [columnnamelist[counttables - 1]] * len(activation_df)
                        if eachtable > 1:
                            df_list[-eachtable]['Country'] = [columnnamelist[eachtable]] * len(df_list[-eachtable])
                    # if counttables ==4:
                    #     df_list[-4]['Country'] = [columnnamelist[0]] * len(df_list[-4])
                    #     df_list[-3]['Country'] = [columnnamelist[1]] * len(df_list[-3])
                    #     df_list[-2]['Country'] = [columnnamelist[2]] * len(df_list[-2])
                    #     activation_df['Country'] = [columnnamelist[3]] * len(activation_df)
                    # if counttables ==3:
                    #     df_list[-3]['Country'] = [columnnamelist[0]] * len(df_list[-3])
                    #     df_list[-2]['Country'] = [columnnamelist[1]] * len(df_list[-2])
                    #     activation_df['Country'] = [columnnamelist[2]] * len(activation_df)
                    # else:
                    #     df_list[-2]['Country'] = [columnnamelist[0]] * len(df_list[-2])
                    #     activation_df['Country'] = [columnnamelist[1]] * len(activation_df)
                    for eachtable in range(counttables - 1):
                        activation_df = activation_df.append(df_list[-(eachtable + 2)], ignore_index=True)

                    # activation_df = activation_df.append(df_list[-2], ignore_index=True)
                    # if counttables == 3:
                    #     activation_df = activation_df.append(df_list[-3], ignore_index=True)
                    # if counttables == 4:
                    #     activation_df = activation_df.append(df_list[-4], ignore_index=True)

                last = ''
                firstcolumn = []
                firstcolumnname = activation_df.columns.tolist()[0]
                lastcolumnname = activation_df.columns.tolist()[-1]
                activation_df[lastcolumnname] = activation_df[lastcolumnname].astype(str, errors='ignore')
                activation_df = activation_df[activation_df[lastcolumnname].apply(lambda x: startprint(x))]
                activation_df = activation_df.reset_index(drop=True)
                countriesInTable = False

                if firstcolumnname == 'Country' or firstcolumnname == 'Countries':
                    secondcolumnname = activation_df.columns.tolist()[1]
                    activation_df = activation_df.rename({secondcolumnname: 'Exporter'}, axis=1)
                elif 'Exporter/producer' in activation_df.columns:
                    activation_df = activation_df.rename({'Exporter/producer': 'Exporter'}, axis=1)
                    temp_column = activation_df.pop('Exporter')
                    activation_df.insert(0, 'Exporter', temp_column)
                    firstcolumnname = 'Exporter'
                elif 'Exporter' in activation_df.columns:
                    temp_column = activation_df.pop('Exporter')
                    activation_df.insert(0, 'Exporter', temp_column)
                else:
                    activation_df = activation_df.rename({firstcolumnname: 'Exporter'}, axis=1)
                    firstcolumnname = 'Exporter'
                    if activation_df[firstcolumnname][0] in all_countries:
                        countriesInTable = True

                activation_df = activation_df[activation_df['Exporter'].apply(lambda x: startprint(x))]

                len_of_act = len(activation_df)
                if countriesInTable:
                    countries = []
                    for i in range(len_of_act):
                        curr = activation_df[firstcolumnname][i]
                        if curr in all_countries:
                            if curr == 'PRC':
                                curr = 'China'
                            last = curr
                            countries.append(curr)
                        else:
                            countries.append(last)
                    activation_df['Country'] = countries
                for i in range(len_of_act):
                    curr = activation_df[firstcolumnname][i]
                    if isinstance(curr, str):
                        if curr == 'PRC':
                            curr = 'China'
                        last = curr
                        firstcolumn.append(curr)
                    else:
                        firstcolumn.append(last)
                activation_df[firstcolumnname] = firstcolumn
                if countriesInTable:
                    activation_df = activation_df[activation_df[firstcolumnname].apply(lambda x: iscountry(x))]
                    activation_df = activation_df.reset_index(drop=True)
                    len_of_act = len(activation_df)
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
                activation_df['DOC'] = [DOC] * len_of_act
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d{1}>(.+?)<h\d{1} id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 5:
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                    # todo: probably fix the order
                    if len(activation_HScodeList) == 6:
                        for i in range(0, len(activation_HScodeList) + 1):
                            if i < 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                            if i == 2:
                                activation_df['HS' + str(i + 1)] = [''] * len_of_act
                            if i > 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i - 1]]* len_of_act
                    if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:

                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                    HSACTLIST = len(activation_HScodeList)
                activation_df['Source'] = [activation_source] * len_of_act

    if activation_df.empty:
        if not initiation_df.empty and not revocation_df.empty:
            combine_ini_rev_list = ["FedReg", "Country", "Year",
                                    "Month", "Date", "AD/CVD", "Action", "DOC", "Source"]
            for eachHS in range(min(HSREVLIST, HSINILIST)):
                combine_ini_rev_list.append("HS" + str(eachHS + 1))
            combine_ini_rev_list = revocation_df.merge(initiation_df, on=list(combine_ini_rev_list), how='outer')
            combine_ini_rev_list['no activation'] = ['1'] * len(combine_ini_rev_list)
            combine_ini_rev_list.to_csv(product + DOC + '_AD.csv', index=False)
            print('only int + rev ----------- AD')
            return
        elif not initiation_df.empty:
            print('only initiation file')
            initiation_df['no activation'] = ['1'] * len(initiation_df)
            initiation_df['no revocation'] = ['1'] * len(initiation_df)
            initiation_df.to_csv(product + DOC + '_AD.csv', index=False)
        elif not revocation_df.empty:
            print('only revocation file --------------- AD')
            revocation_df['no initiation'] = ['1'] * len(revocation_df)
            revocation_df['no activation'] = ['1'] * len(revocation_df)
            revocation_df.to_csv(product + DOC + '_AD.csv', index=False)
        else:
            emptytxt.write(product + ' ' + DOC + '\n')
            print('-------------------missing all 3  AD--------------------------')
        return
    if not initiation_df.empty:
        print('we have initiation files!')
        Petitioner_column = [col for col in initiation_df.columns if 'Petitioner' in col or 'Ptner' in col]
        Petitioner_column.append("Country")
        initiation_df_subset = initiation_df[Petitioner_column]
        if not activation_df.empty:
            activation_df = activation_df.merge(initiation_df_subset, on=["Country"])
        if not revocation_df.empty:
            revocation_df = revocation_df.merge(initiation_df_subset, on=["Country"])

    activation_df_subset = activation_df[["Country", "Exporter", "Producer"]]
    if not initiation_df.empty:
        initiation_df = activation_df_subset.merge(initiation_df, on=["Country"])
    if not revocation_df.empty:
        revocation_df = activation_df_subset.merge(revocation_df, on=["Country"])


    if len(revocation) != 0:
        print('we have revocation file AD')
        combine_act_rev_list = ["FedReg", "Country", "Exporter", "Producer", "Year",
                                "Month", "Date", "AD/CVD", "Action", "DOC", "Source"]
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
        print('missing initiation file ------------ AD')
        combine_act_rev = combine_act_rev.sort_values('Year')
        cols = list(combine_act_rev.columns.values)
        cols.pop(cols.index('Source'))
        combine_act_rev = combine_act_rev[cols + ['Source']]
        combine_act_rev['no initiation'] = ['1']* len(combine_act_rev)
        combine_act_rev.to_csv(product + DOC + '_AD.csv', index=False)
        return

    combine_column = ["Country", "FedReg", "Year", "Month", "Date", "AD/CVD", "Action", "Exporter", "Producer","DOC", "Source"]
    for i in Petitioner_column:
        combine_column.append(i)
    for eachHS in range(min(HSINILIST, HSACTLIST, HSREVLIST)):
        combine_column.append("HS" + str(eachHS + 1))
    combine_int_rest = initiation_df.merge(combine_act_rev, on=list(combine_column), how='outer')
    combine_int_rest = combine_int_rest.sort_values('Year')
    cols = list(combine_int_rest.columns.values)
    cols.pop(cols.index('Source'))
    combine_int_rest = combine_int_rest[cols + ['Source']]
    combine_int_rest.to_csv(product + ' ' + DOC + '_AD.csv', index=False)

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
    webLinkFormat = re.compile(r'"(https://www.federalregister.gov/documents/\d+.+?)"', flags=re.M)
    webLinkList = webLinkFormat.findall(webContent)
    initiation = []
    activation = []
    revocation = []
    productName = product.replace(' ', '-').lower()
    productName = productName.replace('&', 'and')
    productName = productName.replace(',', '')
    for link in webLinkList:
        if productName in link or 'notice-of-implementation' in link or 'countervailing' in link:
            longlink = urllib.request.urlopen(link)
            longwebContent = str(longlink.read())
            titlePattern = re.compile(
                r'<div id="metadata_content_area" class="metadata-content-area">\\n.+<h1>(.+?)<\/h1>',
                flags=re.M)
            oldPattern = re.compile(r'The full text of this document is',
                flags=re.M)
            title = titlePattern.findall(longwebContent)[0]
            oldformat = oldPattern.findall(longwebContent)
            if product not in title:
                continue;
            print(title)
            if 'Pursuant to Court Decision' in title or 'Five-Year' in title:
                continue
            if ('Revocation of' in title and 'Countervailing' in title) or 'Revocation of Orders' in title:
                if 'Consideration of Revocation' in title or ('Countervailing Duty Orders' not in title):
                    continue
                print('END ' + title)
                print(link)

                if len(oldformat) > 0:
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    print('Revocation File is too old')
                    continue
                revocation.append(link)
                revocation_source = link
                revocation_action = 'revocation'
                countryFormat = re.compile(r'(Revocation.+)', flags=re.M)
                revocation_country = countryFormat.findall(title)[0]
                if len(revocation_country) == 0:
                    revocation_country = title
                countries = []
                for c in all_countries:
                    if c in revocation_country:
                        countries.append(c)
                if len(countries) == 0:
                    revocation_country = title
                    for c in all_countries:
                        if c in revocation_country:
                            countries.append(c)
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                revocation_year = dateString[:4]
                revocation_month = dateString[5:7]
                revocation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{3,5})\\n', flags=re.M)
                revocation_FedReg = FedRegFormat.findall(longwebContent)[0]
                revocation_df['Country'] = countries
                revocation_df['Action'] = [revocation_action] * len(countries)
                revocation_df['Year'] = [revocation_year] * len(countries)
                revocation_df['Month'] = [revocation_month] * len(countries)
                revocation_df['Date'] = [revocation_date] * len(countries)
                revocation_df['FedReg'] = [revocation_FedReg] * len(countries)
                revocation_df['AD/CVD'] = ['CVD'] * len(countries)
                revocation_df['DOC'] = [DOC] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        revocation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(revocation_HScodeList) == 5:
                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                    # todo: probably fix the order
                    if len(revocation_HScodeList) == 6:
                        for i in range(0, len(revocation_HScodeList) + 1):
                            if i < 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                            if i == 2:
                                revocation_df['HS' + str(i + 1)] = [''] * len(countries)
                            if i > 2:
                                revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i - 1]] * len(countries)
                    if len(revocation_HScodeList) < 5 or len(revocation_HScodeList) > 6:

                        for i in range(0, len(revocation_HScodeList)):
                            revocation_df['HS' + str(i + 1)] = [revocation_HScodeList[i]] * len(countries)
                    HSREVLIST = len(revocation_HScodeList)

                revocation_df['Source'] = [revocation_source] * len(countries)
                continue

            if 'Preliminary' in title or 'Expedited Review' in title or 'Corrected Notice' in title or 'Changed Circumstances Review' in title or 'Extension of Time Limits' in title:
                continue
            if 'Initiation of Countervailing Duty' in title or ('Initiation of' in title and 'Countervailing' in title):
                if 'Correction to' in title or 'Anti-Circumvention' in title or 'Amendment' in title or 'New Shipper Review' in title or 'Intent To Revoke Orders in Part' in title:
                    continue
                print('INITIATION: ' + title)
                print(link)
                if len(oldformat) > 0:
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    print('INITIATION File is too old')
                    continue
                initiation.append(link)
                initiation_source = link
                initiation_action = 'initiation'
                dateFormat = re.compile(r'Publication Date.+documents/(\d{4}/\d{2}/\d{2})', flags=re.M)
                dateString = dateFormat.findall(longwebContent)[0]
                initiation_year = dateString[:4]
                initiation_month = dateString[5:7]
                initiation_date = dateString[-2:]
                FedRegFormat = re.compile(r'document-citation.+(\d{2}\s[A-Z]{2}\s\d{3,5})\\n', flags=re.M)
                initiation_FedReg = FedRegFormat.findall(longwebContent)[0]
                initiation_petitioners = []
                petitionerFormat1 = re.compile(r'proper\sform\s(?:by)?(?:on behalf of)?(.+)\((?:collectively,?\s)?(?:“)?(?:\w{3}\s)?(?:“)?\wetitioner(?:\w)?(?:")?\)', flags=re.M)
                if len(petitionerFormat1.findall(longwebContent)) != 0:
                    if ',' in petitionerFormat1.findall(longwebContent)[0]:
                        initiation_petitioners = petitionerFormat1.findall(longwebContent)[0].split(",")
                    else:
                        initiation_petitioners = petitionerFormat1.findall(longwebContent)[0].split("and")
                petitionerFormat2 = re.compile(r'proper\sform\s(?:by)?(?:on behalf of)?\s(.+?)\((?:collectively,?\s)?(?:&ldquo;)?(?:\w{3}\s)?(?:&ldquo;)?\wetitioner(?:\w)?&rdquo;\)',
                                               flags=re.M)
                if len(petitionerFormat2.findall(longwebContent)) != 0:
                    if ',' in petitionerFormat2.findall(longwebContent)[0]:
                        initiation_petitioners = petitionerFormat2.findall(longwebContent)[0].split(",")
                    else:
                        initiation_petitioners = petitionerFormat2.findall(longwebContent)[0].split("and")
                countries = []
                for c in all_countries:
                    if c in title:
                        countries.append(c)
                initiation_df['Country'] = countries
                initiation_df['Action'] = [initiation_action] * len(countries)
                initiation_df['Year'] = [initiation_year] * len(countries)
                initiation_df['Month'] = [initiation_month] * len(countries)
                initiation_df['Date'] = [initiation_date] * len(countries)
                initiation_df['FedReg'] = [initiation_FedReg] * len(countries)
                initiation_df['AD/CVD'] = ['CVD'] * len(countries)
                if len(initiation_petitioners) == 0:
                    initiation_df['no petitioner'] = ['1']*len(countries)
                else:
                    for i in range(len(initiation_petitioners)):
                        initiation_df['Petitioner' + str(i + 1)] = [initiation_petitioners[i]] * len(countries)
                        altnameformat = re.compile(r'\((.+?)\)', flags=re.M)
                        altname = ''
                        if len(altnameformat.findall(initiation_petitioners[i])) > 0:
                            altname = altnameformat.findall(initiation_petitioners[i])[0]
                        initiation_df['Ptner' + str(i + 1) + 'AltNm'] = [altname] * len(countries)
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d>(.+?)<h\d id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        initiation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(initiation_HScodeList) == 5:
                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                    if len(initiation_HScodeList) == 6:
                        for i in range(0, len(initiation_HScodeList) + 1):
                            if i < 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                            if i == 2:
                                initiation_df['HS' + str(i + 1)] = [''] * len(countries)
                            if i > 2:
                                initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i - 1]]* len(countries)
                    if len(initiation_HScodeList) < 5 or len(initiation_HScodeList) > 6:

                        for i in range(0, len(initiation_HScodeList)):
                            initiation_df['HS' + str(i + 1)] = [initiation_HScodeList[i]]* len(countries)
                    HSINILIST = len(initiation_HScodeList)
                initiation_df['DOC'] = [DOC] * len(countries)
                initiation_df['Source'] = [initiation_source] * len(countries)
                continue

            if 'Affirmative Final Determination' in title or 'Sunset Review' in title or 'Notice of Countervailing Duty Order: Honey' in title:
                continue
            if 'Countervailing Duty Order' in title:
                if 'Clarification of the Scope'in title or 'Final Affirmative Determination'in title or 'Final Clarification' in title or 'Correction for' in title or 'Correction to' in title or 'Amendment to' in title or 'Changed Circumstance' in title or 'Continuation' in title or 'Pursuant to Court' in title or 'Court Decision' in title or 'Amended' in title:
                    continue
                print('START ' + title)
                print(link)
                if len(oldformat) > 0:
                    tooOldfile.write(product + ' ' + DOC + '\n' + link + '\n')
                    print('activation File is too old')
                    continue
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
                counttables = 1
                if len(activation_df.columns.tolist()) == len(df_list[-2].columns.tolist()) and activation_df.columns[-1] == df_list[-2].columns[-1]:
                    counttables = 2
                    if len(df_list[-3].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-3].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 3
                    if len(df_list[-4].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-4].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 4
                    if len(df_list[-5].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-5].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 5
                    if len(df_list[-6].columns.tolist()) == len(df_list[-2].columns.tolist()) and df_list[-6].columns[-1] == df_list[-2].columns[-1]:
                        counttables = 6
                    countryFormatInTitle = re.compile(r'From(.+)', flags=re.M)
                    activation_countryFormat_in_title = countryFormatInTitle.findall(title)
                    columnnamelist = []
                    if len(activation_countryFormat_in_title) > 0:
                        for c in all_countries:
                            if c in activation_countryFormat_in_title[0]:
                                columnnamelist.append(c)
                    for eachtable in range(counttables):
                        if eachtable == 1:
                            activation_df['Country'] = [columnnamelist[counttables - 1]] * len(activation_df)
                        if eachtable > 1:
                            df_list[-eachtable]['Country'] = [columnnamelist[eachtable]] * len(df_list[-eachtable])
                    for eachtable in range(counttables - 1):
                        activation_df = activation_df.append(df_list[-(eachtable + 2)], ignore_index=True)


                last = ''
                firstcolumn = []
                firstcolumnname = activation_df.columns.tolist()[0]
                lastcolumnname = activation_df.columns.tolist()[-1]
                activation_df[lastcolumnname] = activation_df[lastcolumnname].astype(str, errors='ignore')
                activation_df = activation_df[activation_df[lastcolumnname].apply(lambda x: startprint(x))]
                activation_df = activation_df[activation_df[firstcolumnname].apply(lambda x: startprint(x))]
                activation_df = activation_df.reset_index(drop=True)
                countriesInTable = False

                if firstcolumnname == 'Country' or firstcolumnname == 'Countries':
                    secondcolumnname = activation_df.columns.tolist()[1]
                    activation_df = activation_df.rename({secondcolumnname: 'Exporter'}, axis=1)
                elif 'Exporter/producer' in activation_df.columns:
                    activation_df = activation_df.rename({'Exporter/producer': 'Exporter'}, axis=1)
                    temp_column = activation_df.pop('Exporter')
                    activation_df.insert(0, 'Exporter', temp_column)
                    firstcolumnname = 'Exporter'
                elif 'Exporter' in activation_df.columns:
                    temp_column = activation_df.pop('Exporter')
                    activation_df.insert(0, 'Exporter', temp_column)
                else:
                    activation_df = activation_df.rename({firstcolumnname: 'Exporter'}, axis=1)
                    firstcolumnname = 'Exporter'
                    if activation_df[firstcolumnname][0] in all_countries:
                        countriesInTable = True

                len_of_act = len(activation_df)
                if countriesInTable:
                    countries = []
                    for i in range(len_of_act):
                        curr = activation_df[firstcolumnname][i]
                        if curr in all_countries:
                            if curr == 'PRC':
                                curr = 'China'
                            last = curr
                            countries.append(curr)
                        else:
                            countries.append(last)
                    activation_df['Country'] = countries
                for i in range(len_of_act):
                    curr = activation_df[firstcolumnname][i]
                    if isinstance(curr, str):
                        if curr == 'PRC':
                            curr = 'China'
                        last = curr
                        firstcolumn.append(curr)
                    else:
                        firstcolumn.append(last)
                activation_df[firstcolumnname] = firstcolumn
                if countriesInTable:
                    activation_df = activation_df[activation_df[firstcolumnname].apply(lambda x: iscountry(x))]
                    activation_df = activation_df.reset_index(drop=True)
                    len_of_act = len(activation_df)
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
                activation_df['DOC'] = [DOC] * len_of_act
                SOIformat = re.compile(r'Scope of\s(.+?)</h\d{1}>(.+?)<h\d{1} id=', flags=re.M)
                try:
                    SOI = SOIformat.findall(longwebContent)[1][1]
                except IndexError:
                    SOI = longwebContent
                if len(SOI) > 0:
                    HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{4})', flags=re.M)
                    activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 0:
                        HScodeFormate = re.compile(r'(\d{4}\.\d{2}\.\d{2})', flags=re.M)
                        activation_HScodeList = list(HScodeFormate.findall(SOI))
                    if len(activation_HScodeList) == 5:
                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                    # todo: probably fix the order
                    if len(activation_HScodeList) == 6:
                        for i in range(0, len(activation_HScodeList) + 1):
                            if i < 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                            if i == 2:
                                activation_df['HS' + str(i + 1)] = [''] * len_of_act
                            if i > 2:
                                activation_df['HS' + str(i + 1)] = [activation_HScodeList[i - 1]]* len_of_act
                    if len(activation_HScodeList) < 5 or len(activation_HScodeList) > 6:

                        for i in range(0, len(activation_HScodeList)):
                            activation_df['HS' + str(i + 1)] = [activation_HScodeList[i]]* len_of_act
                    HSACTLIST = len(activation_HScodeList)
                activation_df['Source'] = [activation_source] * len_of_act


    # special for initiation: petitioners
    # special for activation: "Dumping margin","Cash deposit (%)", "Exporter"
    if activation_df.empty:
        if not initiation_df.empty and not revocation_df.empty:
            combine_ini_rev_list = ["FedReg", "Country", "Year",
                                    "Month", "Date", "AD/CVD", "Action", "DOC", "Source"]
            for eachHS in range(min(HSREVLIST, HSINILIST)):
                combine_ini_rev_list.append("HS" + str(eachHS + 1))
            combine_ini_rev_list = revocation_df.merge(initiation_df, on=list(combine_ini_rev_list), how='outer')
            combine_ini_rev_list['no activation'] = ['1'] * len(combine_ini_rev_list)
            combine_ini_rev_list.to_csv(product + DOC + 'CVD.csv', index=False)
            print('only have int + rev ------------------- CVD')
        elif not initiation_df.empty:
            initiation_df['no activation'] = ['1'] * len(initiation_df)
            initiation_df.to_csv(product + DOC + '_CVD.csv', index=False)
            print('only initiation file ---------------- CVD')
        elif not revocation_df.empty:
            revocation_df.to_csv(product + DOC + '_CVD.csv', index=False)
            print('only revocation file -------------- CVD')
        else:
            emptytxt.write(product + ' ' + DOC + '\n')
            print('-------------------missing all 3  CVD--------------------------')
        return
    if len(initiation) != 0:
        print('we have initiation files!')
        Petitioner_column = [col for col in initiation_df.columns if 'Petitioner' in col or 'Ptner' in col]
        Petitioner_column.append("Country")
        initiation_df_subset = initiation_df[Petitioner_column]
        if not activation_df.empty:
            activation_df = activation_df.merge(initiation_df_subset, on=["Country"])
        if not revocation_df.empty:
            revocation_df = revocation_df.merge(initiation_df_subset, on=["Country"])
        # activation_df_subset = activation_df[["Country", "Dumping margin", "Cash deposit (%)", "Exporter"]]
        activation_df_subset = activation_df[["Country", "Exporter", "Producer"]]
        if not initiation_df.empty:
            initiation_df = activation_df_subset.merge(initiation_df, on=["Country"])
        if not revocation_df.empty:
            revocation_df = activation_df_subset.merge(revocation_df, on=["Country"])

    if len(revocation) != 0:
        print('we have revocation file AD')
        combine_act_rev_list = ["FedReg", "Country", "Exporter", "Producer", "Year",
                                "Month", "Date", "AD/CVD", "Action", "DOC", "Source"]
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
        print('missing initiation file ------------ CVD')
        combine_act_rev = combine_act_rev.sort_values('Year')
        cols = list(combine_act_rev.columns.values)
        cols.pop(cols.index('Source'))
        combine_act_rev = combine_act_rev[cols + ['Source']]
        combine_act_rev['no initiation'] = ['1']* len(combine_act_rev)
        combine_act_rev.to_csv(product + DOC + '_CVD.csv', index=False)
        return

    combine_column = ["Country", "FedReg", "Year", "Month", "Date", "AD/CVD", "Action", "Exporter", "Producer","DOC", "Source"]
    for i in Petitioner_column:
        combine_column.append(i)
    for eachHS in range(min(HSINILIST, HSACTLIST, HSREVLIST)):
        combine_column.append("HS" + str(eachHS + 1))
    combine_int_rest = initiation_df.merge(combine_act_rev, on=list(combine_column), how='outer')
    combine_int_rest = combine_int_rest.sort_values('Year')
    cols = list(combine_int_rest.columns.values)
    cols.pop(cols.index('Source'))
    combine_int_rest = combine_int_rest[cols + ['Source']]
    combine_int_rest.to_csv(product +' ' + DOC + '_CVD.csv', index=False)

def changeProductName(product):
    product = product.replace('&', 'and')
    if product == 'Frozen Warm-water Shrimp and Prawns' or product == 'Frozen Or Canned Warm-water Shrimp and Prawns':
        product = 'Frozen Warmwater Shrimp'
    if product == 'Grain-oriented Electrical Steel':
        product = 'Grain-Oriented Electrical Steel'
    if product == 'Seamless Pipe':
        product = 'Seamless Carbon'
    if product == 'Stainless Steel Plate In Coils':
        product = 'Stainless Steel Plate in Coils'
    if product == 'Stainless Steel Sheet & Strip In Coils' or product == 'Stainless Steel Sheet and Strip In Coils':
        product = 'Stainless Steel Sheet and Strip in Coils'
    if product == 'Barbed wire & barbless wire strand':
        product = 'Barbed Wire and Barbless Fencing Wire'
    if product == 'Non-frozen Apple Juice Concentrate':
        product = 'Non-Frozen Apple Juice Concentrate'
    if product == 'Hot-rolled Carbon Steel Flat Products':
        product = 'Hot-Rolled Steel Flat Products'
    if product == 'Low-Enriched Uranium':  # C-428-829
        product = 'Low Enriched Uranium'
    if product == 'Low-enriched Uranium':
        product = 'Low-Enriched Uranium'
    if product == 'Carbon Steel Wire Rod':
        product = 'Carbon and Certain Alloy Steel Wire Rod'
    if product == 'Lawn and Garden Fence Posts':
        product = 'Lawn and Garden Steel Fence Posts'
    if product == 'Tow Behind Lawn Groomer':
        product = 'Tow Behind Lawn Groomers'
    if product == 'Drill Pipe and Drill Collars':
        product = 'Drill Pipe'
    if product == 'Porcelain-on-steel Cooking Ware':
        product = 'Porcelain-on-Steel Cooking Ware'
    if product == 'Top-of-the-stove Stainless Steel Cooking Ware':
        product = 'Top of the Stove Stainless Steel Cooking Ware'
    if product == 'Stainless Steel Butt-weld Pipe Fittings':
        product = 'Stainless Steel Butt-Weld Pipe Fittings'
    if product == 'Internal Combustion Industrial Forklift Trucks':
        product = 'Internal Combustion Forklift Trucks'
    if product == 'Spherical Plain Bearings': #check
        product = 'Antifriction Bearings'
    if product == 'Light-walled Rectangular Tube':
        product = 'Light-Walled Rectangular Welded Carbon Steel Pipe'
    if product == 'Polyethylene Terephthalate (PET) Film':
        product = 'Polyethylene Terephthalate Film'
    if product == 'Corrosion-resistant Carbon Steel Flat Products':
        product = 'Corrosion-Resistant Carbon Steel Flat Products'
    if product == 'Small Diameter Carbon and Alloy Seamless Standard, Line, and Pressure Pipe':
        product = 'Small Diameter Carbon and Alloy Seamless Standard, Line and Pressure Pipe'
    if product == 'Pure Magnesium (ingot)':
        product = 'Pure Magnesium'
    if product == 'Seamless Pipe (small Diameter)':
        product = 'Small Diameter Seamless Carbon'
    if product == 'Carbon Steel Plate':
        product = 'Carbon-Quality Steel Plate'
    if product == 'Large Diameter Seamless Pipe':
        product = 'Large Diameter Carbon'
    if product == 'Small Diameter Seamless Pipe':
        product = 'Small Diameter Carbon'
    if product == 'Pure Magnesium (granular)':
        product = 'Pure Magnesium in Granular'
    if product == 'Non-malleable Cast Iron Pipe Fittings':
        product = 'Non-Malleable Cast Iron Pipe Fittings'
    if product == 'Light?Cwalled Rectangular Pipe and Tube' or product == 'Light-walled Rectangular Pipe and Tube':
        product = 'Light-Walled Rectangular Pipe and Tube'
    if product == 'Coated Paper Suitable For High-Quality Print Graphics Using Sheet-Fed Presses':
        product = 'Coated Paper Suitable for High-Quality Print Graphics Using Sheet-Fed Presses'
    if product == 'Diffusion-Annealed, Nickel-Plated Flat- Rolled Steel Products':
        product = 'Diffusion-Annealed, Nickel-Plated Flat-Rolled Steel Products'
    if product == 'Boltless Steel Shelving Units Prepackaged For Sale':
        product = 'Boltless Steel Shelving Units Prepackaged for Sale'
    if product == '1-Hydroxyethylidene-1, 1-Diphosphonic Acid (HEDP)':
        product = '1-Hydroxyethylidene-1, 1-Diphosphonic Acid'
    if product == 'Dioctyl Terephthalate (DOTP)':
        product = 'Dioctyl Terephthalate'
    if product == 'Cold-Drawn Mechanical Tubing Of Carbon and Alloy Steel':
        product = 'Cold-Drawn Mechanical Tubing of Carbon and Alloy Steel'
    if product == 'Polyethylene Terephthalate Sheet?':
        product = 'Polyethylene Terephthalate Sheet'
    # if product == '':
    #     product = ''
    # if product == '':
    #     product = ''
    # if product == '':
    #     product = ''
    # if product == '':
    #     product = ''
    # if product == '':
    #     product = ''
    return product

for index in range(0, len(DOCarray)):
    # get the type: AD/CVD -- first char in a string
    type = DOCarray[index][0]
    DOC = DOCarray[index]
    product = " ".join([k[:1].upper() + k[1:] if k.lower() != 'and' else k for k in productArray[index].split()])
    product = changeProductName(product)
    print(DOC)
    print(product)
    if (type == 'A'):
        AntiDumping(DOC, product)

    elif (type == 'C'):
        Countervailing(DOC, product)

tooOldfile.close()
emptytxt.close()
# noinittxt.close()
# noacttxt.close()
# norevocatiotxt.close()


