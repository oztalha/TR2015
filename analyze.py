# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:37:21 2015

@author: Talha
"""

import pandas as pd
from unidecode import unidecode
import matplotlib.pyplot as plt

# A great dataset of past Turkish elections is available at
# Gunes Murat Tezcur's website http://www.luc.edu/faculty/gtezcur/data.html
# The dataset: http://www.luc.edu/faculty/gtezcur/files/TEPLWeb.xlsx

df11 = pd.read_csv('data/TEPLWeb.csv',nrows=81,
        usecols = ['PROV1NAME', 'VALID11','AKPP11', 'CHPP11', 'MHPP11','BGMP11'])
df11 = df11.replace('AFYON','AFYONKARAHISAR')
df11 = df11.replace('SANLI URFA','SANLIURFA')
df11 = df11.rename(columns={'BGMP11':'HDPP11'})
df11['OTHERS11'] = df11.apply(lambda x: 100 - sum(x[2:]),axis=1)

df15 = pd.read_csv('data/TR2015.csv')
df15 = df15.rename(columns={'province':'PROVINCE'})
df15 = df15[~df15['PROVINCE'].str.contains('\d')]
df15['PROVINCE'] = df15['PROVINCE'].apply(lambda x: unidecode(x).upper())
df15 = df15.drop('others',axis=1)
df15['OTHERS'] = df15.apply(lambda x: 100 - sum(x[1:]),axis=1)

# combine the both !
df = df15.merge(df11,left_on='PROVINCE',right_on='PROV1NAME')
df = df.drop('PROV1NAME',axis=1)

cols = [col for col in df.columns if col not in ['PROVINCE', 'VALID11']]
df[cols] = df[cols]/100
df.to_csv('data/TR_11_15.csv',index=False)

# plot 2011-2015 comparison with self (for each party)
plt.style.use('ggplot')
parties = ['AKP','CHP','MHP','HDP']
for p in parties:
    p11 = p + 'P11'
    lim = max(df[p].max(),df[p11].max()) + 5
    ax = df.plot(x=p11, y=p, kind='scatter', figsize=(15,15),xlim=(0,lim),ylim=(0,lim))
    df.apply(lambda x: ax.annotate(x['PROVINCE'], (x[p11],x[p]),
                xytext=(-30, 7), textcoords='offset points',fontsize=9), axis=1);
    ax.set_xlabel(p+" 2011 Vote Shares",fontsize=14);
    ax.set_ylabel(p+" 2015 Vote Shares",fontsize=14);
    ax.set_title(p+' 2015 vs 2011 Vote Shares',fontsize=18,x=0.5, y=0.95)
    ax.plot([0,1],[0,1], transform=plt.gca().transAxes);
    plt.savefig('charts/'+p+'.PNG',bbox_inches='tight')
    
#plotly graphs
import plotly.plotly as py
from plotly.graph_objs import *
for p in parties:
    p11 = p + 'P11'
    lim = max(df[p].max(),df[p11].max()) + 5
    data = Data([Scatter(x=df[p11],y=df[p])])
    layout = Layout(title=p+' 2015 vs 2011 Vote Shares',
                    autosize=True,
                    xaxis=XAxis(title=p+" 2011 Vote Shares"),
                    yaxis=YAxis(title=p+" 2015 Vote Shares"))
    fig = Figure(data=data,layout=layout)
    py.iplot(fig)