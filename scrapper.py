#-------scraper libraries code ----------------
import pandas as pd
import numpy as np
import re
import os
import warnings
warnings.filterwarnings('ignore')
import json
import csv
import io
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time
#------scraper libraries code end-------------

#---Scraping url code---------------------------------------
def scrap(url):
    
    df = pd.DataFrame(columns = ['Website','City','img','img_url','Category','Item','mrp','discount','item_url','Quantity','Price'])
    qty=[]
    price = []
    name=[]
    cat=[]
    img_url=[]
    img=[]
    disc=[]
    mrp=[]
    prod_url=[]
    for k in range(0,6):
        headers = {
        'authority': 'catalog.service.frendy.in:3000',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://shop.frendy.in',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://shop.frendy.in/',
        'accept-language': 'en-US,en;q=0.9',
        }

        #d = '{"categories":"64","ipp":"20","paginator":"1"}'
        #data = '{"categories":"64","ipp":"20","paginator":'+ "{}".format(i)+'}'

        d = '{"categories":"64","ipp":"20","paginator":'+ "{}".format(k)+'}'

        response = requests.post('https://catalog.service.frendy.in:3000/api/product/list', headers=headers, data=d)
        data = json.loads(response.text)
        data2 = data['productDefinitions']
        url = 'https://shop.frendy.in/#/product-detail?productId='

        for i in range(len(data['productDefinitions'])):
            for j in range(len(data2[i]['Variations'])):
                try:
                    qty.append(data2[i]['Variations'][j]['Attributes'][0]['ProductAttributeValue']['value']) # for this nan have to be filled using regex
                except:
                    qty.append(np.nan)
                try:
                    price.append(data2[i]['Variations'][j]['ProductPrices'][0]['frendyPrice'])
                except:
                    price.append(np.nan)
                              #i              #j
                try:
                    name.append(data2[i]['identifier'])
                except:
                    name.append(np.nan)
                try:    
                    cat.append(data2[i]['Categories'][0]['identifier'])
                except:
                    cat.append(np.nan)
                try:
                    img_url.append(data2[i]['imageAbsolutePath'])
                except:
                    img_url.append(np.nan)
                try:
                    img.append(data2[i]['image'])
                except:
                    img.append(np.nan)
                try:
                    disc.append(data2[i]['Variations'][j]['ProductPrices'][0]['discount'])
                except:
                    disc.append(np.nan)
                try:
                    mrp.append(data2[i]['Variations'][j]['ProductPrices'][0]['mrp'])
                except:
                    mrp.append(np.nan)
                try:
                    prod_url.append(url+str(data2[i]['id']))
                except:
                    prod_url.append(np.nan)

                
                
    df['img'] = pd.Series(img)
    df['img_url'] = pd.Series(img_url)
    df['Category'] = pd.Series(cat)
    df['Item'] =pd.Series(name)
    df['mrp'] = pd.Series(mrp)
    df['discount'] =pd.Series(disc)
    df['item_url'] = pd.Series(prod_url)
    df['Quantity'] = pd.Series(qty)
    df['Price'] = pd.Series(price)
    df['Website'] = 'Frendy'
    df['City'] = 'Ahmedabad'
    df['Item'] = df['Item'].apply(lambda x: re.sub('[0-9]{1,3}[' '] [a-zA-Z]{1,5}','',x))
    df['Quantity']=df.Quantity.apply(lambda x: str(x).replace(' ','') )
    
    df.reset_index(inplace=True)
    df1 = df["Category"].unique().tolist()
    df.drop('index',axis=1,inplace=True)
    df.drop_duplicates(['Item','Price'],inplace=True)
    df.to_csv('frendy_grocery.csv')
    return df1

#---Scraping url code end-----------------------------------


