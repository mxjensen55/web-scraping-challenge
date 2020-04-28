
#dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
from splinter import Browser


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser= init_browser()

    #create empty dictionary to hold all scraped mars info
    mars={}

    #NASA Mars News
    ##grab header and text
    news_url = 'https://mars.nasa.gov/news/'
    response=requests.get(news_url)
    #grab headline and text
    headline_soup = bs(response.text, 'lxml')
    headline = headline_soup.find('div', class_ = 'content_title').text.strip()
    paragraph = headline_soup.find('div', class_ = 'rollover_description_inner').text.strip()
    #amend dictionary with data
    mars["headline"] = headline
    mars["paragraph"] = paragraph
    #visit image url
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_id('full_image')
    time.sleep(2)
    browser.find_link_by_partial_text('more info').click()
    html = browser.html
    image_soup = bs(html, "lxml")
    img_url = image_soup.find('figure', class_ = 'lede')
    img_url=img_url.a.img['src']
    featured_img_url = "https://www.jpl.nasa.gov" + img_url

    #add img url to mars info dictionary
    mars["featured_image"]=featured_img_url

    #grab latest weather tweet

    tweet_url="https://twitter.com/marswxreport?lang=en"
    response=requests.get(tweet_url)
    tweet_soup=bs(response.text, 'lxml')
 
    mars_weather_tweet = tweet_soup.find_all('div', class_ = "js-tweet-text-container")

    for tweet in mars_weather_tweet:
        if tweet.text.strip().startswith('InSight sol'):
            mars_weather = tweet.text.strip()
    #add mars tweet to open mars info dictionary

    mars["tweet"]=mars_weather


    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    mars_df = pd.read_html(facts_url)
    mars_df = (mars_df[0])
    mars_df.columns= ['Description', 'Value']
    mars_df=mars_df.set_index('Description')
    mars_df = mars_df.to_html(classes='mars')
    table_data = mars_df.replace('\n', ' ')
    
    mars["mars_table"]=table_data

    #Mars Hemispheres
    hemi_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html = browser.html
    mars_hemis=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'lxml')
        tag = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ tag
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    mars["hemispheres"]=mars_hemis

    # Close the browser after scraping
    browser.quit()
    #return the completed dictionary
    return mars
