#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import datetime




# colors for bar plot
CSSE_color = '#F9B79C'
WHO_color = '#99D6E4'
  
#using this list to match the name from WHO to JHU
name_match_dict = { 'Brunei Darussalam':'Brunei' ,
                    'Côte d’Ivoire':"Cote d'Ivoire",
                   'Russian Federation':'Russia',
                   'Republic of Korea':'South Korea',
                   'Korea, South':'South Korea',
                   'Republic of Moldova':'Moldova',
                   'United States of America':'USA',
                   'US':'USA',
                   'United Republic of Tanzania':'Tanzania',
                   'occupied Palestinian territory':'West Bank and Gaza',
                   'Democratic Republic of the Congo':'Congo (Kinshasa)',
                   "Lao People's Democratic Republic":'Laos',
                   'The United Kingdom':'United Kingdom',
                   'Myanmar':'Burma',
                   'Syrian Arab Republic' : 'Syria',
                   'Congo' : 'Congo (Brazzaville)'
                   
                   # ('',''),
                   # ('',''),
                   # ('',''),
                   # ('',''),
                   # ('','')
                   }

:


CSSE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
WHO_URL='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/who_covid_19_situation_reports/who_covid_19_sit_rep_time_series/who_covid_19_sit_rep_time_series.csv'




#Read data from Github
WHO_data = pd.read_csv(WHO_URL,index_col=False, encoding = 'utf-8')
CSSE_data = pd.read_csv(CSSE_URL,index_col=False)




# process CSSE data

CSSE_copy = copy.copy(CSSE_data)

CSSE_data.drop(['Province/State','Lat', 'Long'],axis=1,inplace=True)
CSSE_data.replace(name_match_dict,inplace=True)
CSSE_country_sums = CSSE_data.groupby('Country/Region').sum()

# process WHO data
WHO_copy = copy.copy(WHO_data)

string_cols = ['Province/States', 'Country/Region', 'WHO region']
num_cols = list(WHO_data.columns)
for col in string_cols:
    num_cols.remove(col)


WHO_data.replace(name_match_dict,inplace=True)
  

# list of tuples containing values that need to be fixed in WHO_data
#                # index   column    replacement
who_fixlist = [(   17,    '3/5/2020',      418       )] 

who_startrow = 40 # first row in WHO_data where confirmed cases start  (not totalss or deaths)
who_endrow = 253 #Last row in WHO_data where confirmed cases ends

for tup in who_fixlist:
    WHO_data.loc[tup[0],tup[1]] = tup[2]

WHO_data[num_cols] = WHO_data[num_cols].apply(pd.to_numeric)

w_rows = WHO_data.shape[0]

WHO_data.drop(['WHO region','Province/States'],axis=1,inplace=True)
WHO_data.drop(   list(np.arange(0,who_startrow)) + list(np.arange(who_endrow+1,w_rows)) ,inplace=True)

WHO_country_sums = WHO_data.groupby('Country/Region').sum()


# # One import thing: Two data set must have the same number of columns



WHO_data = WHO_data.reset_index().drop(columns = ['index', '1/21/2020']).set_index('Country/Region')




CSSE_country_sums = CSSE_country_sums.drop(columns = ['5/14/20'])




same_name = []
for i in WHO_data.index:
    if i in CSSE_country_sums.index:
        same_name.append(i)
len(same_name)




a = list(range(0, len(WHO_data.columns)*4, 4))
b = [x - 2 for x in a]




#plot all comparisons and save
for i in same_name:
    fig, ax = plt.subplots(figsize = (20,10), dpi =300)
    plt.bar(a,CSSE_country_sums.loc[i, :],width=2,color=CSSE_color, edgecolor = 'k', label= 'Johns Hopkins University CSSE')
    plt.bar(b,WHO_data.loc[i, :],width=1.8,color=WHO_color,edgecolor = 'k', label= 'WHO')
    labels = [-100, 'Jan', 'Feb', 'March', 'April', 'May'] #Need change this accoding to plot
    ax.set_xticklabels(labels, fontsize = 20)
    ax.legend(loc='upper left',fontsize=15)

    ax.set_title(i, Fontsize = '30')
    fig.savefig('E:/COVID-19/CSSE_vs_WHO' + i + '.png')
    

