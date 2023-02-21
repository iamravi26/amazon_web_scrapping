import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def get_title(soup):
    try:
        title = soup.find('span',attrs={'id':'productTitle'}).string.strip()
    
    except AttributeError:
        title=""
    
    return title

def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':'a-price'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except:
            price = ""

    return price
 
def get_rating(soup):
    try:
        rating=soup.find('span',attrs={'class':'a-icon-alt'}).string.strip()
    
    except AttributeError:
        rating= ""
    return rating


def  get_reviews(soup):
    try:
        reviews_count= soup.find('span',attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        reviews_count=""
    return reviews_count

def get_instock(soup):
    try:
        instock = soup.find('span',attrs={'class':'a-size-medium a-color-success'}).string.strip()
    except AttributeError:
        instock= "" 
    return instock


if __name__=="__main__":

    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    URL = "https://www.amazon.in/s?k=earphones&crid=2FNOB0D9DG72C&sprefix=ear%2Caps%2C185&ref=nb_sb_ss_ts-doa-p_3_3"

    webpage = requests.get(URL,headers= HEADERS)

    soup = BeautifulSoup(webpage.content,"html.parser")

    links = soup.find_all('a',attrs={'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    links_list=[] 

    for link in links:
        links_list.append(link.get('href'))

    d = {'title':[], 'price':[], 'rating':[], 'reviews':[], 'instock':[]}

    for link in links_list:


        new_webpage = requests.get("https://amazon.in"+link, headers= HEADERS)

        new_soup= BeautifulSoup(new_webpage.content,"html.parser")



        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_reviews(new_soup))
        d['instock'].append(get_instock(new_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_scrapping.csv", header=True, index=False)
    print(amazon_df)




