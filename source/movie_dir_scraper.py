#!/usr/bin/env python
# coding: utf-8

# # Top 100 Movie in 2021 Scraping 

# ## System setup 
# 
# Before we start, make sure to install the required libraries
#     
#     pip install bs4
#     pip install selenium
# 
# Since the website has some javascript rendered HTML content, we'll be using Selenium for scraping the content loaded dynamically by javascript. For this,you would also need to download a selenium supported browser webdriver.
# 
# e.g. For Chrome, download the appropriate webdriver from here: http://chromedriver.chromium.org/downloads, unzip it and save in current directory.

# In[8]:


from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import time


# ## Input URL 

# In[9]:


dir_url = 'https://www.rottentomatoes.com/top/bestofrt/?year=2021'
base_url = 'https://www.rottentomatoes.com'


# In[10]:


#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)


# In[11]:


#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup


# In[12]:


def scrape_dir_page(dir_url,driver):
    print ('-'*20,'Scraping directory page','-'*20)
    movie_links = []
    soup = get_js_soup(dir_url,driver)
    table = soup.find('table', class_='table')
    for link_holder in table.find_all('a',class_='unstyled articleLink'): #get list of all <div> of class 'name'
#         print(link_holder)
        link = link_holder['href'] #get url
        #url returned is relative, so we need to add base url
        movie_links.append(base_url + link) 
    print ('-'*20,'Found {} movie urls'.format(len(movie_links)),'-'*20)
    return movie_links


# It might take a few minutes to get all the urls

# In[13]:


movie_links = scrape_dir_page(dir_url,driver)


# In[14]:


movie_links


# It takes a few minutes to scrape all the urls

# In[15]:


def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')


# In[16]:


movie_urls_file = 'movie_urls.txt'
write_lst(movie_links, movie_urls_file)


# In[ ]:




