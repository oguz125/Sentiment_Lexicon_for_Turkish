# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 08:54:50 2018

@author: oguz1
"""
import os
import csv
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
from sklearn.model_selection import train_test_split

corpus=pd.read_csv('corpus.csv',error_bad_lines=False,names=['rating','yorum'])
train, test = train_test_split(corpus, test_size=.2)



kelimeler=[]
for yorum in corpus:
    for kelime in [i.lower() for i in mt.tokenize(yorum[1]) if i.isalpha()]:
        kelimeler.append(kelime)
    kelimeler=list(set(kelimeler))
url='http://www.tdk.gov.tr/index.php?option=com_gts&arama=gts&kelime='
turkce_sozluk=[]
counter=0
for kelime in kelimeler[40693:]:
    try:
        req=requests.get(url+kelime)
    except:
        time.sleep(30)
        try:
            req=requests.get(url+kelime)
        except:
            time.sleep(90)
            try:
                req=requests.get(url+kelime)
            except:
                print('FAIL '+counter)
                break
    if BeautifulSoup(requests.get(url+kelime).text, 'html.parser').find("table", {"id": "hor-minimalist-a"})!=None:
        turkce_sozluk.append(kelime)
    counter=counter+1
    if counter in [i*1000 for i in range(40)]:
        print(str(len(turkce_sozluk))+': '+str(counter)+' is done '+str(len(kelimeler)-counter)+' is to go!')
path=os.path.dirname(os.path.realpath(__file__))
csv_file=path+'turkce_sozluk.csv'
with open(csv_file, 'w',encoding="utf-8-sig") as myfile:
    wr = csv.writer(myfile)
    for x in turkce_sozluk:
        wr.writerow([x])
turkce_sozluk= list(reversed(sorted(turkce_sozluk, key=len)))
turkce_sozluk=[kelime for kelime in turkce_sozluk if len(kelime)>2]
turkce_sozluk_ekler={key:None for key in turkce_sozluk}
temp=kelimeler
for key in turkce_sozluk_ekler:
    turkce_sozluk_ekler[key]=[item for item in temp if item.startswith(key)]
    temp=[i for i in temp if i not in turkce_sozluk_ekler[key]]
'''
frekans=dict(zip(turkce_sozluk,np.zeros(len(turkce_sozluk))))
for yorum in corpus:
    for kelime in [i.lower() for i in mt.tokenize(yorum[1]) if i.isalpha()]:
        frekans[kelime]=frekans[kelime]+1
frekans_list=sorted([[key,frekans[key]] for key in frekans], key=lambda key: key[1],reverse=True)
'''