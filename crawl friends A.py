# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:21:46 2020

@author: Jerry
"""
from selenium import webdriver
import pandas as pd
import re
import time
import json 

account = 'qiaolurangn@126.com'
password = 'di054330'
your_id = 100009419083778
file_path = "Facebook Friends.csv"
# =============================================================================
# 登入
# =============================================================================
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values':{'notifications': 2}}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(r"C:\Users\Jerry\chromedriver.exe",options=options)
driver.get('https://www.facebook.com/')
driver.find_element_by_id('email').send_keys(account)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_id('u_0_b').click()
time.sleep(3)
# =============================================================================
# profile
# =============================================================================
url = f'https://www.facebook.com/profile.php?id={your_id}'
driver.get(url)
htmltext = driver.page_source

pattern = "{\"status\":2.*}}}"
allFriends = re.findall(pattern,htmltext)
friends = allFriends[0].split("status")
final_friends = []

def is_id_repeated(id_):
    for friend in final_friends:
        if friend["id"] == id_:
            return True
    return False

for friend in friends:
    try:
        start = friend.find("{")
        end = friend.find("}}")+1
        friend = json.loads(friend[start:end+1])
        if is_id_repeated(friend["id"]):
            continue
        friend['profile_url'] = "https://www.facebook.com/profile.php?id="+friend["id"]
        friend['profile_picture'] = friend['profile_picture']["uri"]
        final_friends.append(friend)
    except:
        pass

data = pd.DataFrame(final_friends)
data.to_csv(file_path,encoding="utf_8_sig",index=False)
