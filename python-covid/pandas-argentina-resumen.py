from __future__ import unicode_literals  # or use u"unicode strings"
import numpy as np
import scipy as sc
from scipy.stats import norm

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
params = {'legend.fontsize': 13, 'legend.handlelength': 2}
plt.rcParams.update(params)
font = {'family' : 'Arial', 'weight':'bold', 'size'   : 12}
matplotlib.rc('font', **font)

import re
import pandas as pd
import requests, io
from pandas_coronavirus_config import *

print('reading time series')
def get_data(_url):
	#c=pd.read_csv(s)
	_s=requests.get(_url)
	df=pd.read_csv(io.StringIO(_s.content.decode('utf-8')), error_bad_lines=False)
	return df

def process_x(mydataframe):
	date = []
	count = []
	#for x in mydataframe.columns.to_list():
	#	date.append(x)
	#	count.append( mydataframe[x].values[0] )

	#d = {'date': date, 'count': count}
	#df4 = pd.DataFrame(data=d)
	#print(df4.head())
	#df4 = df4[3:]
	df4 = mydataframe
	df4['fecha'] = pd.to_datetime(df4['fecha'],format='%d/%m/%Y')
	df4['fecha'] = df4['fecha'].dt.strftime('%d/%m/%Y')
	return df4

df = get_data(arg_historico)
_arg = df

_a = process_x(_arg)
#s = _a['tot_casosconf']
s = _a['nue_casosconf_diff']
ss = s.values.tolist()

r = np.zeros(len(ss))
for i in range(len(ss)):
	r[i] = ss[len(ss) - i-1]

s = np.array(r)

_len = len(s)
print(_len)
cumsum = s.sum()

# mu=1;sigma=0.25
mu = cumsum/_len
mean =  (s-mu)**2
mean1 = np.mean(s)
std = np.std(s)
variance = (1/_len) * mean.sum()# Its wrong as its a cumulative sum
sigma=np.sqrt(variance)

print("mu = ", mu)
print("mean = ", mean)
print("variance = ", variance)
print("sigma = ", sigma)

print ("Mu - Mean < 0.01", abs(mu - np.mean(s)) < 0.01   )# must be true
print ("Sigma - Std < 0.01", abs(sigma - np.std(s, ddof=1)) < 0.01  ) # must be true

fig, ax = plt.subplots()
plt.tight_layout()

count, bins, ignored = ax.hist(s, bins= 60, density=True, stacked=False, cumulative=False, alpha=0.65, lw=0.8, edgecolor='black', color='green')

print(ignored)

onesigma = 1 # s.sum()
deviation = onesigma/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) )
df = pd.DataFrame({'Value': bins, 'Deviation': deviation })

df.plot(kind='line', x='Value', y='Deviation', ax=ax, lw=1.8, color='red')

#error = [deviation+0.1, deviation-0.1]
#ax.errorbar(df['Value'], df['Deviation'], yerr=error, fmt='-o')

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


#plt.savefig('C:/users/diego2/desktop/figure_8_arg.png')
plt.show()
