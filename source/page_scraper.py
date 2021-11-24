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
tomatometer_rating = []

for i in url:

    page = requests.get(i)
    soup = BeautifulSoup(page.content, 'html.parser')

    content = ""

    #Title

    title = soup.find('h1', attrs={'data-qa': 'score-panel-movie-title'})
    content = content + title.string.strip() + " "
    title_content.append(title.string.strip())


    # tomatometer rating
    scores = soup.find("score-board")
    tomato_score = scores["tomatometerscore"] + "%"
    tomatometer_rating.append(tomato_score)

    #Where to watch
    affiliate = soup.find_all("a", "affiliate__link")
    for data in affiliate:
        content = content + data["data-affiliate"] + " "

    #Movie Info
    synopsis = soup.find('div', attrs={'id': 'movieSynopsis'})
    content = content + synopsis.string.strip() + " "
    synopsis_content.append(synopsis.string.strip())

    #Movie Rating (if it exists on the page)
    rating = soup.find(text="Rating:")
    if rating:
        rating = rating.findNext('div').contents[0]
        rating = rating.string.strip()
        rating = re.sub(r"\s+", " ", rating) #remove tabs and line breaks
        content = content + rating + " "

    #Movie Genre (if it exists on the page)
    genre = soup.find('div', {'class' :'meta-value genre'})
    if genre:
        genre = genre.string.strip()
        genre = re.sub(r"\s+", " ", genre) #remove tabs and line breaks
        content = content + genre + " "

    #Cast
    cast = soup.find_all("span", "characters subtle smaller")
    for data in cast:
        content = content + data["title"] + " "

    #reviews
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

write_lst(title_content,"data/titles.txt")
write_lst(synopsis_content,"data/synopsis.txt")
write_lst(tomatometer_rating,"data/ratings.txt")

print("Scraping completed and files saved under 'data' folder")
