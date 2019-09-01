# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

def init_browser():
    # Choose the executable path to driver
    executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)
     
def scrape():
    browser = init_browser()

    # create mars dictionary for mongo
    mars_data = {}

    # 1.NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html

    news_soup = bs(html, 'html.parser')

    news_title = news_soup.find('div', class_='content_title').find('a').text
    news_para = news_soup.find('div', class_='article_teaser_body').text

    # add to mars_data
    mars_data["news_title"] = news_title
    mars_data["news_para"] = news_para

    # 2.JPL Mars Space Images
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    html_image = browser.html

    image_soup = bs(html_image, 'html.parser')

    image = image_soup.find("img", class_="thumb")["src"]

    featured_image_url = "https://www.jpl.nasa.gov" + image
    
    # add to mars_data
    mars_data["featured_image_url"] = featured_image_url

    # 3. Mars Weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html_weather = browser.html

    weather_soup = bs(html_weather, 'html.parser')

    mars_weather_tweets = weather_soup.find_all('div', class_='js-tweet-text-container')

    for tweet in mars_weather_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            mars_weather = weather_tweet
            break
        else: 
            pass

    # add to mars_data
    mars_data["mars_weather"] = mars_weather

    # 4. Mars Fact
    mars_facts = pd.read_html('https://space-facts.com/mars/')
    mars_df = mars_facts[1]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    table = mars_df.to_html()

    # add to mars_data
    mars_data["table"] = table

    # 5. Mars Hemispheres
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    html_hemispheres = browser.html

    hemispheres_soup = bs(html_hemispheres, 'html.parser')
    hemispheres_items = hemispheres_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for hemi_img in hemispheres_items:
    
        img_title = hemi_img.find('h3').text
        partial_img_url = hemi_img.find('a', class_='itemLink product-item')['href']
    
        browser.visit('https://astrogeology.usgs.gov/' + partial_img_url)
        html_hemispheres = browser.html
    
        hemispheres_soup = bs(html_hemispheres, 'html.parser')
        img_url = 'https://astrogeology.usgs.gov/' + hemispheres_soup.find('img', class_='wide-image')['src']
    
        hemisphere_image_urls.append({"title" : img_title, "img_url" : img_url})
    
    # add to mars_data
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    # return mars_data dict
    print(mars_data["featured_image_url"])

    return mars_data

if __name__ == "__main__":
    scrape()