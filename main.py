import os
from bs4 import BeautifulSoup
import time
import sys
import numpy as np
import pandas as pd
import regex as re
import requests
import lxml
from lxml.html.soupparser import fromstring
import prettify
import numbers

#set some display settings for notebooks
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#add headers in case you use chromedriver (captchas are no fun); namely used for chromedriver
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}



def scrape(content):

        soup = BeautifulSoup(content, 'html.parser')

        df = pd.DataFrame()
        urls=[]

        address = soup.find_all(class_= 'list-card-addr')
        price = list(soup.find_all (class_='list-card-price'))
        price = [x.get_text() for x in price]
        beds = list(soup.find_all("ul", class_="list-card-details"))
        details = soup.find_all ('div', {'class': 'list-card-details'})
        home_type = soup.find_all ('div', {'class': 'list-card-footer'})
        last_updated = soup.find_all ('div', {'class': 'list-card-top'})
        brokerage = list(soup.find_all(class_= 'list-card-brokerage list-card-img-overlay',text=True))
        link = soup.find_all (class_= 'list-card-link')

        df['prices'] = price
        df['address'] = address
        df['beds'] = beds

        for link in soup.find_all("article"):
            href = link.find('a',class_="list-card-link")
            if(href==None): continue;
            addresses = href.find('address')
            addresses.extract()
            urls.append(href)

        #import urls into a links column
        df['links'] = urls
        df['links'] = df['links'].astype('str')

        #remove html tags
        df['links'] = df['links'].replace('<a class="list-card-link list-card-link-top-margin" href="', ' ', regex=True)
        df['links'] = df['links'].replace('" tabindex="0">\n\n</a>', ' ', regex=True)

        df['prices'] = df['prices'].astype('str')
        df['address'] = df['address'].astype('str')
        df['beds'] = df['beds'].astype('str')

        #remove tags
        df['prices'] = df['prices'].replace('<div class="list-card-price">', ' ', regex=True)
        df['address'] = df['address'].replace('<address class="list-card-addr">', ' ', regex=True)
        df['prices'] = df['prices'].replace('</div>', ' ', regex=True)
        df['address'] = df['address'].replace('</address>', ' ', regex=True)

        df['beds'] = df['beds'].replace('<ul class="list-card-details">', ' ', regex=True)
        df['beds'] = df['beds'].replace('<abbr class="list-card-label">', ' ', regex=True)
        df['beds'] = df['beds'].replace('<li class="">', ' ', regex=True)
        df['beds'] = df['beds'].replace('</li>', ' ', regex=True)
        df['beds'] = df['beds'].replace('<!-- -->', ' ', regex=True)
        df['beds'] = df['beds'].replace('ba', ' ', regex=True)
        df['beds'] = df['beds'].replace('bds', ' ', regex=True)
        df['beds'] = df['beds'].replace('bd', ' ', regex=True)
        df['beds'] = df['beds'].replace('sqft', ' ', regex=True)
        df['beds'] = df['beds'].replace('</abbr>', ' ', regex=True)
        test=df['beds'].str.split(expand=True)
        #print(test[0],test[1],test[2])
        df['beds']=test[0]
        df['baths']=test[1]
        df['sq_feet']=test[2]
        #df['beds'] = df['beds'].replace('Studio</li><li>', '0 ', regex=True)



        df['prices'] = df['prices'].str.strip()
        df['address'] = df['address'].str.strip()
        df['beds'] = df['beds'].str.strip()
        #df['prices'] = df['prices'].str.replace(r'\D', '')

        #print(df['beds'][0])
        print(df.to_string())
