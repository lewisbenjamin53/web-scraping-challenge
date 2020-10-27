# Dependencies
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # dictionary to store mars data for mongo database
    dic = {}

    # news
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    articles = news_soup.find_all('li', class_= 'slide')
    latest_article = articles[0]
    latest_title = latest_article.find('div', class_= 'content_title').text
    latest_text = latest_article.find('div', class_= 'article_teaser_body').text
    dic['latest_title'] = latest_title
    dic['latest_text'] = latest_text

    #image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    base_splint_url = 'https://www.jpl.nasa.gov'
    splint_url = base_splint_url + image_soup.find('a', class_= "button fancybox")["data-fancybox-href"]
    dic['splint_url'] = splint_url

    #facts
    table_url = "https://space-facts.com/mars/"
    panda_tables = pd.read_html(table_url)
    time.sleep(1)
    table_df = panda_tables[0]
    table_df.columns = ["Type", "Measurement"]
    table_df_str = table_df.to_html()
    dic["table"] = table_df_str

    #hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(1)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    hemi = hemi_soup.find_all('div', class_= 'item')
    hemi_img_urls = {}
    for x in hemi:
        title = x.find('h3').text
        hemi_url = "https://astrogeology.usgs.gov" + x.find('a', class_='itemLink product-item')['href']
        hemi_img_urls[title] = hemi_url
    dic["hemi_img_urls"] = hemi_img_urls
    
    print(dic)

    return dic


    