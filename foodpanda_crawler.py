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
from re import search
import time
# =============================================================================
#   find the homepage of each city
# =============================================================================
home_url = "https://www.foodpanda.com.tw/?gclid=Cj0KCQjw0YD4BRD2ARIsAHwmKVm3oXrgkoplYvn26S82dzkJBWHej058x8Dy5DNDigpPbRNqu7VPc_0aAtU7EALw_wcB"
response = requests.get(home_url)
soup = BeautifulSoup(response.text)
all_a = soup.find_all("a",class_="city-tile")
all_link = [a.get("href") for a in all_a ]
# =============================================================================
#   foodpanda-find all vendor
# =============================================================================
url = "https://www.foodpanda.com.tw"+all_link[0]
response = requests.get(url)
soup = BeautifulSoup(response.text)
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
    
vendors_info = pd.DataFrame(vendors)
vendors_info["id"] = [i for i in range(1,len(vendors_info)+1)]
                            
# =============================================================================
#  foodpanda - find menu
# =============================================================================
base_url = "https://www.foodpanda.com.tw"
menus = []
for id_,link,title in zip(vendors_info["id"].values,
                          vendors_info["link"].values,
                          vendors_info["name"].values):
    print("Crawling "+title)
    
    response = requests.get(base_url+link)
    soup = BeautifulSoup(response.text)
    
    dishes_section = soup.find_all("div",class_="dish-category-section")
    for section in dishes_section:
        #restaurant menu-category
        category = section.find("h2",class_="dish-category-title").text
        dishes = section.find("ul",class_="dish-list").find_all("li")
        for dish in dishes:
            menu = {}
            menu["id"] = id_
            menu["category"] = category
            #restaurant menu-name
            menu["name"] = dish.find("h3").find("span").text
            #menu-price
            menu["price"] = dish.find("span",class_="price p-price").text.strip()
            menus.append(menu)
    time.sleep(0.3)

vendors_menu = pd.DataFrame(menus)
# =============================================================================
# clean data
# =============================================================================
vendors_info[vendors_info.isnull()].sum()
vendors_menu[vendors_menu.isnull()].sum()

def extract_number(str_num):
    pattern = "[\d,]+.[\d]{2}"
    return search(pattern, str_num).group(0)

vendors_menu.price = vendors_menu.price.apply(extract_number)
vendors_menu.price = vendors_menu.price.apply(lambda price:price.replace(",",""))

vendors_info.count = vendors_info["count"].astype(int)
vendors_menu.price = vendors_menu["price"].astype(float)
# =============================================================================
#  save data
# =============================================================================
with pd.ExcelWriter("food-panda.xlsx") as writer:
    vendors_info.to_excel(writer,sheet_name="店家評分")
    vendors_menu.to_excel(writer,sheet_name="店家菜單")
    