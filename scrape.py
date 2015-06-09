# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 19:17:16 2015

@author: Talha
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

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
# Manually added BOM using Notepad++ to make MS Excel happy
