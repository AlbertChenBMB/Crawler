# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 10:40:15 2020

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
