from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

dir_url = 'https://www.rottentomatoes.com/top/bestofrt/?year=2021'
base_url = 'https://www.rottentomatoes.com'


#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)


#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup



def scrape_dir_page(dir_url,driver):
    print ('-'*20,'Scraping directory page','-'*20)
    movie_links = []
    soup = get_js_soup(dir_url,driver)
    table = soup.find('table', class_='table')
    for link_holder in table.find_all('a',class_='unstyled articleLink'): #get list of all <div> of class 'name'

        link = link_holder['href'] #get url
        #url returned is relative, so we need to add base url
        movie_links.append(base_url + link) 
    print ('-'*20,'Found {} movie urls'.format(len(movie_links)),'-'*20)
    return movie_links





movie_links = scrape_dir_page(dir_url,driver)

def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')

movie_urls_file = 'movie_urls.txt'
write_lst(movie_links, movie_urls_file)





