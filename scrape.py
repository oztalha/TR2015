# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 19:17:16 2015

@author: Talha
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

# il secim sonuclari
url = 'http://www.yenisafak.com.tr/secim-2015/secim-sonuclari'
resource = requests.get(url)
soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
# kill all script, style, sub, sup and b elements
for script in soup(["script", "style", "sup", "sub", "b"]):
    script.extract()    # rip it out 
tables = soup.find_all(class_='table-data') # 3 tables
data = tables[1].find_all('span')
data.extend(tables[2].find_all('span')[7:]) #skip the 2nd header row
df = pd.DataFrame(columns=('province','AKP', 'CHP','MHP','HDP','others'))
for i in range(1,int(len(data)/7)):
    i = 7*i
    try:
        if data[i].text[0].isalpha(): 
            city = data[i].text.strip()
            province = [city] # province name
        else:
            province = [' '.join([city,data[i].text])]
        for j in range(2,7): # party shares
            province.append(float(data[i+j].text.replace(',','.')))
        df.loc[len(df)+1]=province
    except Exception as e:
        print('[ERROR]', e)
    df.to_csv('data/TR2015.csv',index=False,encoding='utf-8')


# ilce secim sonuclari http://secim.haberler.com sitesinden toplandi
urls = pd.read_csv('data/ilceler_link.csv',
                   usecols=["ilceler.href"],squeeze=True).tolist()
df = pd.DataFrame(columns=('il','ilce', 'AKP', 'CHP','MHP','HDP','OTHERS',
  'AKPV', 'CHPV','MHPV','HDPV','OTHERSV'))
parties = ['AK PARTİ', 'CHP','MHP','HDP']
for url in urls:
    try:
        resource = requests.get(url)
        soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
        # kill all script, style, sub, sup and b elements
        for script in soup(["script", "style", "sup", "sub"]):
            script.extract()    # rip it out 
        il = soup.find(class_='right-div-sonuc').find('div').text.split(' ')[0]
        ilce = soup.find(class_='ana-parti-listesi-baslik').text.split(' 2')[0]
        sonuclar = soup.findAll(class_='ana-parti-listesi-content')
        OTHERS = 0
        OTHERSV = 0
        for sonuc in sonuclar:
            parti = sonuc.find(class_='ana-parti-listesi-parti').text.strip()
            yuzde = float(sonuc.find(class_='ana-parti-listesi-sayısal-brd'
              ).text.strip(' %').replace(',','.'))/100
            oy = int(sonuc.find(class_='ana-parti-listesi-sayısal'
              ).text.strip().replace('.',''))
            if parti in parties:
                if parti == 'AK PARTİ':
                    AKP = yuzde
                    AKPV = oy
                elif parti == 'CHP':
                    CHP = yuzde
                    CHPV = oy
                elif parti == 'MHP':
                    MHP = yuzde
                    MHPV = oy
                elif parti == 'HDP':
                    HDP = yuzde
                    HDPV = oy
                else:
                    print('Error in parties !')
            else:
                OTHERS += yuzde
                OTHERSV += oy
        df.loc[len(df)+1]= [il,ilce,AKP,CHP,MHP,HDP,OTHERS,AKPV,CHPV,MHPV,HDPV,OTHERSV]             
    except Exception as e:
        print(url,e)

    df.to_csv('data/TR2015_ILCELER.csv',index=False,encoding='utf-8')

    