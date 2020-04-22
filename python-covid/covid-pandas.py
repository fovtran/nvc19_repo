from __future__ import unicode_literals  # or use u"unicode strings"
import numpy as np
import scipy as sc
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests, io

url = 'https://github.com/CSSEGISandData/COVID-19/raw/master/who_covid_19_situation_reports/who_covid_19_sit_rep_time_series/who_covid_19_sit_rep_time_series.csv'

confirmed='https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

deaths='https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

print('reading time series')
s=requests.get(url).content
#c=pd.read_csv(s)

df=pd.read_csv(io.StringIO(s.decode('utf-8')))

sample1 = df.loc[:247, '1/21/2020']
sample2 = df.loc[:247, '4/3/2020']
df2 = df.iloc[:, 1:10]
c_names = df2.iloc[:247, :]
cols = df2.columns
items = [{labels: cols} for labels, cols in df2.items()]

arg = df.loc[df['Country/Region'] == 'Argentina']
arg_dict = arg.to_dict()
date = []
count = []
for x in arg.columns.to_list():
	date.append(x)
	count.append( arg[x].values[0] )

d = {'date': date, 'count': count}
df4 = pd.DataFrame(data=d)
totals = df4[3:]
totals['date'] = pd.to_datetime(totals['date'],format='%m/%d/%Y')
totals['date'] = totals['date'].dt.strftime('%m/%d/%Y')

#result = [f(x, y) for x, y in zip(df['1/21/2020'], df['4/3/2020'])]
#print(result)
#for row in df.itertuples(index=True, name='Pandas'):
#	print (getattr(row, "Confirmed"))
#for index, row in df.itercolumns():
#	print(row['Italy'])
    #print(row['Argenina'], row['Italy'])
