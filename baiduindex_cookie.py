# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import Image
import pickle

def get_cookie():
	driver=webdriver.Chrome()
	driver.get('http://index.baidu.com/?tpl=trend&word=%B9%C7%C3%DC%B6%C8%D2%C7')
	e1 = driver.find_element_by_id("TANGRAM_12__userName")
	e1.send_keys("plus0318")
	e2 = driver.find_element_by_id("TANGRAM_12__password")
	e2.send_keys("PLus820828")
	e3 = driver.find_element_by_id("TANGRAM_12__submit")
	e3.click()
	cookies = driver.get_cookies()  
	driver.quit()
	return cookies


def save_cookies(cookies):
	pickle.dump(cookies, open("cookies/cookies.pkl","wb"))

def open_page():
	driver=webdriver.Chrome()
	driver.get("http://index.baidu.com")
	cookies = pickle.load(open("cookies/cookies.pkl", "rb"))
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.get("http://index.baidu.com/?tpl=trend&word=%B9%C7%C3%DC%B6%C8%D2%C7")
open_page()	
#~ cookies = get_cookie()
#~ save_cookies(cookies)
