# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:23:58 2018

@author: oguz1
"""
#import os
import requests
from bs4 import BeautifulSoup
import csv
import time
import concurrent.futures

#A simple get function with multiple tries
def get_url_data(url, max_tries=3):
    remaining_tries = max_tries
    while remaining_tries > 0:
        try:
            return requests.get(url)
        except:
            time.sleep(10)
        remaining_tries = remaining_tries - 1
    return None


    
#A function to retrieve comments and ratings given urls for individual movies

def comment(urls):
    ret=[]
    prev_url=''
    for url in urls:
        for i in range(200):
            rating_temp=[]
            yorum_temp=[]
            page=get_url_data(url+'?page='+str(i+1))
            if (page is None) or page.url==prev_url:
                break           
            soup = BeautifulSoup(page.text, 'html.parser')
            for item in soup.findAll('div',{'class':'review-card-review-holder'}):
                rating=item.find('span',{'class':'stareval-note'}).text.split(',')
                rating=int(rating[0])+int(rating[1])/10
                rating_temp.append(rating)
            for item in soup.findAll('div',{'class':'content-txt review-card-content'}):
                yorum=item.text.strip()
                yorum_temp.append(yorum)
            if len(yorum_temp)==0:
                break
            if len(yorum_temp)==len(rating_temp):
                ret.extend([[rating_temp[i],yorum_temp[i]] for i in range(len(yorum_temp))]) 
            prev_url=page.url
    return ret


if __name__ == '__main__':
        #Retrieve data from url book
    with open('url_book.csv') as file:
        urls=csv.reader(file)
        url_book=[row[0] for row in urls if len(row)==1]
    output_filename = 'corpus.csv'
    with open(output_filename,'w') as myfile:
        pass
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as e:
        futures = []
        for i in list(range(int(len(url_book)/100)+1)):
            f = e.submit(comment, url_book[i*100:(i+1)*100])
            futures.append(f)
        
        try:
            j = 1
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                with open(output_filename,'a') as myfile:
                    wr=csv.writer(myfile)
                    for x in data:
                        wr.writerow(x)
                print("%d finished" % j)
                j += 1
        except KeyboardInterrupt:
            for fut in futures:
                if not fut.done():
                    # this will not be executed as cancelling the parent gather cancels child futures
                    print('Cancelling: ', fut)
                    fut.cancel()
                

      



#Save the comments     
#path=os.path.dirname(os.path.realpath(__file__))
#csv_file = path+'\\corpus.csv' 
#with open(csv_file, 'w',encoding="utf-8-sig") as myfile:
#    wr = csv.writer(myfile)
#    for x in corpus:
#        wr.writerow(x)