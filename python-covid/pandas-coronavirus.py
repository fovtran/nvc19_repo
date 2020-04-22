from __future__ import unicode_literals  # or use u"unicode strings"
import numpy as np
import scipy as sc
from scipy.stats import norm

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests, io
from pandas_coronavirus_config import *

print('reading time series')
s=requests.get(url).content
#c=pd.read_csv(s)

df=pd.read_csv(io.StringIO(s.decode('utf-8')))

def process_x(mydataframe):
	date = []
	count = []
	for x in mydataframe.columns.to_list():
		date.append(x)
		count.append( mydataframe[x].values[0] )

	d = {'date': date, 'count': count}
	df4 = pd.DataFrame(data=d)
	print(df4.head())
	df4 = df4[3:]
	df4['date'] = pd.to_datetime(df4['date'],format='%m/%d/%Y')
	df4['date'] = df4['date'].dt.strftime('%m/%d/%Y')
	return df4

_global = df.loc[df['Province/States'] == 'Confirmed']
_deaths = df.loc[df['Province/States'] == 'Deaths']
_arg = df.loc[df['Country/Region'] == 'Argentina']
_usa = df.loc[df['Country/Region'] == 'United States of America']


_d = process_x(_deaths)
_g = process_x(_global)
_a = process_x(_arg)
_us = process_x(_usa)

print("Global\n", _g.describe())
#print()
#print("Deaths\n", _d.describe())
#print()
#print("Argentina\n", _a.describe())

#for a in _a:
#	print(a)

series = {'date': _g['date'].to_list(), 'global': _g['count'].to_list(), 'deaths': _d['count'].to_list(), 'arg': _a['count'].to_list(), 'us': _us['count'].to_list()}
rr = pd.DataFrame(series, columns=['date', 'global', 'deaths', 'arg', 'us'])

# Comparison
np.array([rr['global']==_g['count'].to_list()])

#ax = rr.plot(x='date', ls='-', lw=0.9)
#ax.grid(True)
#plt.show()
#s = norm.pdf(r)
s = rr['us']

_len = len(s)
cumsum = s.sum()

# mu=1;sigma=0.25
mu = cumsum/_len
mean =  (s-mu)**2
variance = (1/_len) * mean.sum()# Its wrong as its a cumulative sum
sigma=np.sqrt(variance)

print("mu = ", mu)
print("mean = ", mean)
print("variance = ", variance)
print("sigma = ", sigma)

print ("Mu - Mean < 0.01", abs(mu - np.mean(s)) < 0.01   )# must be true
print ("Sigma - Std < 0.01", abs(sigma - np.std(s, ddof=1)) < 0.01  ) # must be true

#df = pd.DataFrame({'Column1': data[:, 0], 'Column2': data[:, 1]})
fig, ax = plt.subplots()

count, bins, ignored = ax.hist(s, bins= 90, density=True, stacked=True, cumulative=False, alpha=0.65, lw=0.8, edgecolor='black', color='green')

print(ignored)

onesigma = 1 # s.sum()
df = pd.DataFrame({'Value': bins, 'Deviation': onesigma/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ) })

df.plot(kind='line', x='Value', y='Deviation', ax=ax, lw=1.8, color='red')

# Revisar luego...
min_ylim, max_ylim = plt.ylim()
ax.axvline(mu, color='orange', linestyle='dashed', linewidth=3)
plt.text(mu*1.08, max_ylim*1.95, '$\mu$: {:.2f}'.format(mu))

ax.axvline(mu+sigma*onesigma, color='orange', linestyle='dashed', linewidth=3)
plt.text(mu+sigma*onesigma, max_ylim*0.9, '$\mu$ + $\sigma$: {:.2f}'.format(mu+sigma))

ax.set_axisbelow(True)
ax.minorticks_on()

ax.grid(which='major', linestyle='-', linewidth='0.5', color='navy')
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()
