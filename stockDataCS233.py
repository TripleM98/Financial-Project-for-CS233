# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import chromedriver_binary
import string

FB_Income= 'https://finance.yahoo.com/quote/FB/financials?p=FB'
FB_Balance= 'https://finance.yahoo.com/quote/FB/balance-sheet?p=FB'
FB_Statistic= 'https://finance.yahoo.com/quote/FB/key-statistics?p=FB'

driver = webdriver.Safari()  #as long as you have webdriver installedl, you can replace Safari with any other browser. I could not get it to work with chrome or brave though

driver.get(FB_Income)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml') #click stop session after
closingprice = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
features= soup.find_all('div', class_='D(tbr)')

headers = []
temp_list = []
label_list = []
final = []
index = 0

#create headers
for item in features[0].find_all('div', class_='D(ib)'):
    headers.append(item.text)

#statement contents
while index <= len(features)-1:
    #filter for each line of the statement
    temp = features[index].find_all('div', class_='D(tbc)')
    for line in temp:
        #each item adding to a temporary list
        temp_list.append(line.text)
    #temp_list added to final list
    final.append(temp_list)
    #clear temp_list
    temp_list = []
    index+=1
    
df = pd.DataFrame(final[1:])
df.columns = headers

#function to make all values numerical (or - for NaNs)
def convert_to_numeric(column):
    first_col = [i.replace(',','') for i in column]
    second_col = [i.replace('-','') for i in first_col]
    final_col = pd.to_numeric(second_col)   
    return final_col

for column in headers[1:]:    
    df[column] = convert_to_numeric(df[column])
    
fb_income = df.fillna('-')

driver = webdriver.Safari()  #as long as you have webdriver installedl, you can replace Safari with any other browser. I could not get it to work with chrome or brave though

driver.get(FB_Balance)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml') #click stop session after

features= soup.find_all('div', class_='D(tbr)')

headers = []
temp_list = []
label_list = []
final = []
index = 0

#create headers
for item in features[0].find_all('div', class_='D(ib)'):
    headers.append(item.text)

#statement contents
while index <= len(features)-1:
    #filter for each line of the statement
    temp = features[index].find_all('div', class_='D(tbc)')
    for line in temp:
        #each item adding to a temporary list
        temp_list.append(line.text)
    #temp_list added to final list
    final.append(temp_list)
    #clear temp_list
    temp_list = []
    index+=1
    
balance= soup.find_all('div', class_='D(tbhg)')
df = pd.DataFrame(final[1:])
df.columns = headers

#function to make all values numerical (or - for NaNs)
def convert_to_numeric(column):
    first_col = [i.replace(',','') for i in column]
    second_col = [i.replace('-','') for i in first_col]
    final_col = pd.to_numeric(second_col)   
    return final_col

for column in headers[1:]:    
    df[column] = convert_to_numeric(df[column])
    
    
fb_balance= df.fillna('-')

#THIS IS THE CODE TO RETRIEVE THE STATISTICS FROM FACEBOOK. STILL NEEDS TO BE WORKED ON.
driver = webdriver.Safari()  #as long as you have webdriver installedl, you can replace Safari with any other browser. I could not get it to work with chrome or brave though
driver.get(FB_Statistic)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml')
stats_table = soup.find_all("div", class_='Mstart(a) Mend(a)')
df = pd.read_html(str(stats_table),header=0)
stats= pd.concat(df, sort=False)