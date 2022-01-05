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
import htmltext


req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
   city = 'nj/'
   url = f'https://www.zillow.com/homes/for_sale/{city}'
   urls=[url]

   for i in range(2,11):
       urls.append(url + f'{i}_p/')

   for url in urls:
       r=s.get(url,headers=req_headers)
       soup=BeautifulSoup(r.content,'html.parser');

   res=pd.DataFrame()
