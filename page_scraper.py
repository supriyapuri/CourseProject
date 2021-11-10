import requests
import re
from bs4 import BeautifulSoup

#Open txt file with urls
with open("data/movie_urls.txt") as f:
    url = f.readlines()

pages = []

#Iterate through each url
title_content = []
synopsis_content = []
for i in url:
    page = requests.get(i)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    content = ""

    #Title

    title = soup.find('h1', attrs={'data-qa': 'score-panel-movie-title'})
    content = content + title.string.strip() + " "
    title_content.append(content)
    #print(title_content)
    
    #Where to watch
    affiliate = soup.find_all("a", "affiliate__link")
    for data in affiliate:
        content = content + data["data-affiliate"] + " "

    #Movie Info
    synopsis = soup.find('div', attrs={'id': 'movieSynopsis'})
    content = content + synopsis.string.strip() + " "
    synopsis_content.append(content)

    attributes = soup.find_all('div', attrs={'data-qa': 'movie-info-item-value'})

    rating = attributes[0].string.strip()
    rating = re.sub(r"\s+", " ", rating) #remove tabs and line breaks
    content = content + rating + " "
    genre = attributes[1].string.strip()
    genre = re.sub(r"\s+", " ", genre) #remove tabs and line breaks
    content = content + genre + " "

    #Cast
    cast = soup.find_all("span", "characters subtle smaller")
    for data in cast:
        content = content + data["title"] + " "

    reviews = soup.find_all("critic-review-bubble")
    for rev in reviews:
        content = content + rev['reviewquote'] + " "

    pages.append(content.strip())

def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')

output = 'data/data.dat'
write_lst(pages,output)
