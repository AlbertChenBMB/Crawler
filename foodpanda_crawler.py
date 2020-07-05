# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:44:21 2020

@author: Jerry
"""


# =============================================================================
# import 
# =============================================================================
import requests
from bs4 import BeautifulSoup,element
import pandas as pd
from selenium import webdriver
import re
import time
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
# =============================================================================
#   find the homepage of each city
# =============================================================================
home_url = "https://www.foodpanda.com.tw/?gclid=Cj0KCQjw0YD4BRD2ARIsAHwmKVm3oXrgkoplYvn26S82dzkJBWHej058x8Dy5DNDigpPbRNqu7VPc_0aAtU7EALw_wcB"
response = requests.get(home_url)
soup = BeautifulSoup(response.text)
all_a = soup.find_all("a",class_="city-tile")
all_link = [a.get("href") for a in all_a ]
# =============================================================================
#   foodpanda-find the all vendor
# =============================================================================
url = "https://www.foodpanda.com.tw"+all_link[0]
response = requests.get(url)
soup = BeautifulSoup(response.text)
all_vendor = soup.find_all("li")

# =============================================================================
#   foodpanda-find all vendor
# =============================================================================
all_li = soup.find("ul",class_="vendor-list").children
all_vendor = []
for v in all_li:
    if isinstance(v,element.Tag):
        all_vendor.append(v)
   
vendors = []
for vendor in all_vendor:
    v = {}
    #restaurant link
    v["link"] = vendor.find("a").get('href')
    #restaurant photo
    pic_url = vendor.find("div").get("data-src")
    v["pic_url"] = pic_url[:pic_url.find("?")]
    #restaurant name
    v["name"] = vendor.find("span",class_="name fn").text
    #restaurant star
    try:
        v["rating"] = vendor.find("span",class_="rating").find("strong").text
        v["count"] = vendor.find("span",class_="count").text.strip()
    except:
        v["rating"] = "NA"
        v["count"] = 0
    
    try:
        v["tag"] = vendor.find("span",class_="multi-tag").text
    except:
        v["tag"] = "NA"
    vendors.append(v)
vendors_info = pd.DataFrame(vendor)
vendors_info["id"] = [i for i in range(1,len(vendors_info)+1)]
                            
# =============================================================================
#  foodpanda - find menu
# =============================================================================
base_url = "https://www.foodpanda.com.tw"
vendors_menu = []
for id_,link,title in zip(vendors_info["id"].values,
                          vendors_info["link"].values,
                          vendors_info["name"].values):
    print("title)
    menu = {}
    menu["id"] = id_
    
    response = requests.get(base_url+link)
    soup = BeautifulSoup(response.text)
    
    dishes = soup.find_all("div",class_="dish-category-section")
    for dish in dishes:
        #restaurant menu-category
        menu["category"] = dish.find("h2",class_="dish-category-title").text
        #restaurant menu-name
        menu["name"] = dish.find("h3").find("span").text
        #menu-price
        menu["price"] = dish.find("span",class_="price p-price").text.strip()
    vendors_menu.append(menu)
    time.sleep(0.5)

# =============================================================================
#  ubereat
# =============================================================================
url = "https://www.ubereats.com/tw/feed?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFOCU4NyVCQSVFNSU4QyU5NyVFOCVCQiU4QSVFNyVBQiU5OSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpVWi1XZlhLcFFqUVIwajRnZ1RvRDg5QSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wNDc2MzMzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjUxNjIzMjQlN0Q%3D"
driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source)
soup.find_all("h3")
soup.find_all("img")

driver.find_element_by_css_selector('input[TEXT=myCheckBox]').click()

url = "https://www.ubereats.com/tw/feed?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFOCU4NyVCQSVFNSU4QyU5NyVFOCVCQiU4QSVFNyVBQiU5OSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpVWi1XZlhLcFFqUVIwajRnZ1RvRDg5QSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyNS4wNDc2MzMzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTIxLjUxNjIzMjQlN0Q%3D"
response = requests.get(url)
soup = BeautifulSoup(response.text)
soup

soup.find("div",class_="e8 g2 g3").find("img").find("img").get("src")
soup.find_all(class_="e8 g2 g3")

soup.find_all("h3")
soup.find_all("img")

# =============================================================================
# 
# =============================================================================
url = "https://www.ubereats.com/tw/taipei/food-delivery/%E8%80%81%E8%B3%B4%E8%8C%B6%E6%A3%A7-%E5%8F%B0%E5%8C%97%E6%9D%BE%E5%B1%B1%E5%BA%97/pe-58e0bTC2RMb0othzLYQ"
response = requests.get(url)
soup = BeautifulSoup(response.text)
soup.find_all("a")[15]
