import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.rottentomatoes.com/m/nomadland")
soup = BeautifulSoup(page.content, 'html.parser')

#"Where to watch"
affiliate = soup.find_all("a", "affiliate__link")
affiliateList = []
for data in affiliate:
    affiliateList.append(data["data-affiliate"])

print(affiliateList)

#Movie Info
synopsis = soup.find('div', attrs={'id': 'movieSynopsis'})
synopsis = synopsis.string.strip()

print(synopsis)

#TODO -- Some attributes not mapping due to extra html tags
#TODO -- Not all pages have the same movie info
attributes = soup.find_all('div', attrs={'data-qa': 'movie-info-item-value'})

rating = attributes[0].string.strip()
genre = attributes[1].string.strip()
language = attributes[2].string.strip()
distributor = attributes[9].string.strip()
sound = attributes[10].string.strip()
aspectratio = attributes[11].string.strip()
print(rating)
print(genre)
print(language)
print(distributor)
print(sound)
print(aspectratio)

#Cast
castList = []
cast = soup.find_all("span", "characters subtle smaller")
for data in cast:
    castList.append(data["title"])

print(castList)
