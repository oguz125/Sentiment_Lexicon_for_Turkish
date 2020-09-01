# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 20:56:25 2018

@author: apolat
"""
import time 
import requests
import csv
from bs4 import BeautifulSoup

#Fn for trying to get url data with a specified maximum number of trials and a time gap between trials
def get_url_data(url, max_tries=3):
    remaining_tries = max_tries
    while remaining_tries > 0:
        try:
            return requests.get(url)
        except:
            time.sleep(10)
        remaining_tries = remaining_tries - 1
    return None



#Creating the url book of movies / the number 500 is arbitrary and greater than the maximum number of movies in a list
url_book=[]

for k in range(1072):
    url='http://www.beyazperde.com/filmler/tum-filmleri/kullanici-puani/?page='+str(k+1)
    page = get_url_data(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for item in soup.findAll('div',{'class':'data_box'}):
        if item.findAll('span',{'class':'stareval stars_medium'})[2].find('span',{'class':'note'}) is None:
            continue
        link='http://www.beyazperde.com'+item.find('a')['href']+'kullanici-elestirileri/'
        url_book.append(link)
    if k%11==0:
        print('%.0f percent complete' %(int(k/11)))
url_book=list(set(url_book))  

#saving to .csv
with open('url_book.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    for x in url_book:
        wr.writerow([x])
     
        
