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
    data = Data([Scatter(x=df[p11],y=df[p],mode='markers',
                         text=df['PROVINCE'])])
    layout = Layout(title=p+' 2015 vs 2011 Vote Shares',
                    autosize=True,
                    xaxis=XAxis(title=p+" 2011 Vote Shares"),
                    yaxis=YAxis(title=p+" 2015 Vote Shares"))
    fig = Figure(data=data,layout=layout)
    py.iplot(fig,fileopt='new')
    
    

# ilce level analysis: outputs TR_11_15_ilce.csv
# https://github.com/mertnuhoglu/secim_verileri/blob/master/data/memurlarnet/genel/collected/genel_secim_oylar.csv
df11 = pd.read_csv('data/genel_secim_oylar.csv')
df11 = df11[df11['yil']==2011]
df15 = pd.read_csv('data/TR2015_ILCELER.csv')
plaka = pd.read_table('data/plaka.tsv',header=None,names=['il','kod'])
# fix non-matching city and party names
# df15[~df15['il'].isin(plaka['il'])]['il'].unique()
plaka = plaka.replace('İçel','Mersin')
plaka = plaka.replace('Afyon','Afyonkarahisar')
kodil = dict(zip(plaka.kod, plaka.il)) #for handiness
ilkod = dict(zip(plaka.il, plaka.kod)) #for handiness
df15 = df15.replace('K.Maraş','Kahramanmaraş')
df15 = df15.merge(plaka)
df11 = df11.replace('AK Parti','AKP')
df11 = df11.replace('BĞMZ','HDP')
df11 = df11.rename(columns={'il':'kod'})

# fix non-matching ilce names
df11[~df11['ilce'].isin(df15['ilce'])]['ilce'].unique()
df15[~df15['ilce'].isin(df11['ilce'])]['ilce'].unique()
df11 = df11.apply(lambda x: x.replace('Merkez',kodil[x.il]),axis=1)
df11 = df11.replace('Didim (Yenihisar)','Didim')
df11 = df11.replace('Devrakani','Devrekani')
df11 = df11.replace('Aydın','Efeler')
df11 = df11.replace('Denizli','Merkezefendi')
df11 = df11.replace('Mardin','Artuklu')
df11 = df11.replace('Aydınlar','Tillo')
df11 = df11.replace('Trabzon','Ortahisar')
df11 = df11.replace('Akköy','Pamukkale')
df11 = df11.replace('Ordu','Altınordu')
df11 = df11.replace('Bahşılı','Bahşili')
df11 = df11.replace('Mihalıçcık','Mihalıççık')
df11 = df11.replace('Samandağı','Samandağ')
df11 = df11.replace('Muğla','Menteşe')
df15 = df15.replace('19.May','19 Mayıs')

df11 = ilce_updater(df11,df15,'Van',['İpekyolu','Tuşba'])
df11 = ilce_updater(df11,df15,'Balıkesir',['Altıeylül','Karesi'])
df11 = ilce_updater(df11,df15,'Hatay',['Antakya', 'Arsuz', 'Defne', 'Payas'])
df11 = ilce_updater(df11,df15,'Kahramanmaraş',['Dulkadiroğlu', 'Onikişubat'])
df11 = ilce_updater(df11,df15,'Manisa',['Şehzadeler', 'Yunusemre'])
df11 = ilce_updater(df11,df15,'Tekirdağ',['Ergene', 'Kapaklı', 'Süleymanpaşa'])
df11 = ilce_updater(df11,df15,'Şanlıurfa',['Eyyübiye','Haliliye', 'Karaköprü'])
df11 = ilce_updater(df11,df15,'Zonguldak',['Zonguldak','Kilimli', 'Kozlu'])
df11 = ilce_updater(df11,df15,'Fethiye',['Fethiye','Seydikemer'])

df11[~df11['ilce'].isin(df15['ilce'])]['ilce'].unique() #'Kargı'
df15[~df15['ilce'].isin(df11['ilce'])]['ilce'].unique() #['Bahçelievler', 'Fatih', 'Malatya']

grouped = df11.groupby(by=['kod','ilce'])
df11 = grouped.apply(getVoteShares).reset_index()
dfilce = df11.merge(df15, on=['kod','ilce'],suffixes=('11','15'))
dfilce.to_csv('data/TR_11_15_ilce.csv',index=False)

parties = ['AKP', 'CHP', 'HDP', 'MHP', 'OTHERS']
#2011 vote shares (according tp dfilce dataset)
for p in parties:
    print((dfilce[p+'11']*dfilce['VOTES11']).sum() / dfilce['VOTES11'].sum())

def ilce_updater(df11,df15,oldilce,new_ilces):
    pop15 = 0
    for i in new_ilces:
        pop15 += df15[df15['ilce']==i][[p+'V' for p in parties]].sum().sum()
    for i in new_ilces:
        pop11 = df11[df11['ilce']==oldilce]['VOTES11'].iloc[0]
        weight = df15[df15['ilce']==i][[p+'V' for p in parties]].sum().sum() / pop15 
        z = df11[df11['ilce']==oldilce].iloc[0]
        z['ilce'] = i
        z['VOTES11']=int(pop11*weight)
        df11 = df11.append(z,ignore_index=True)
    df11 = df11.drop(df11[df11['ilce']==oldilce].first_valid_index())
    return df11


def getVoteShares(g):
    oy = g.Oy.sum()
    AKP = CHP = MHP = HDP = fourSum = 0
    share = {'AKP':0,'CHP':0,'MHP':0,'HDP':0}
    for k in share.keys():
        if g[g.Parti==k].any().any():
            share[k] = float(g[g.Parti==k]['Oy']) / oy
            fourSum += int(g[g.Parti==k]['Oy'])
    share['OTHERS'] = float(oy - fourSum) / oy
    share['VOTES11'] = oy
    return pd.Series(share)