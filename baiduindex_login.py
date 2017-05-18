# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import Image
import time
import os
import random
from urllib import quote,unquote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
import pickle
import requests
import Queue

class BaiduIndex(object):

	def __init__(self):
		self.numdict = self.get_numberdict()
		keys = list()
		vals = list()
		for k, v in self.numdict.items():
			keys.append(k)
			vals.append(v)
		self.keys = keys
		self.vals = vals

		tof = self.judgment()
		if tof == False:
			self.change_cookies()
		#~ dcap = dict(DesiredCapabilities.PHANTOMJS)
		#~ dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
		#~ self.driver=webdriver.PhantomJS(executable_path='/usr/bin/phantomjs', desired_capabilities= dcap)
		#~ self.driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
		self.driver=webdriver.Chrome()
		self.driver.get("http://index.baidu.com")
		cookies = pickle.load(open("cookies/cookies.pkl", "rb"))
		for cookie in cookies:
			if cookie.has_key('expiry'):
				try:
					driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry')})
				except:
					for i in cookie.keys():
						if cookie[i] == 'index.baidu.com':
							cookie[i] = '.index.baidu.com'
					self.driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry')})
			else:
				self.driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path')})

	def judgment(self):
		cookies = pickle.load(open("cookies/cookies.pkl", "rb"))
		s = requests.Session()
		for cookie in cookies:
			s.cookies.set(cookie['name'], cookie['value'])
		response = s.get("http://index.baidu.com/?tpl=trend&word=%B9%C7%C3%DC%B6%C8%D2%C7")
		bodyStr = response.text
		response.close()
		ff = bodyStr.find('ctlName="word"')
		if ff != -1:
			return True
		else:
			return False

	def change_cookies(self):
		#~ dcap = dict(DesiredCapabilities.PHANTOMJS)
		#~ dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
		#~ self.driver=webdriver.PhantomJS(executable_path='/usr/bin/phantomjs', desired_capabilities= dcap)
		driver=webdriver.Chrome()
		#~ driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
		driver.get('http://index.baidu.com/?tpl=trend&word=%B9%C7%C3%DC%B6%C8%D2%C7')
		e1 = driver.find_element_by_id("TANGRAM_12__userName")
		e1.send_keys("这里填写你的账号")
		e2 = driver.find_element_by_id("TANGRAM_12__password")
		e2.send_keys("这里填写你的密码")
		e3 = driver.find_element_by_id("TANGRAM_12__submit")
		e3.click()
		cookies = driver.get_cookies()
		driver.quit()
		pickle.dump(cookies, open("cookies/cookies.pkl","wb"))

	# 拿到数字和文本组合的向量字典
	def get_numberdict(self):
		numdict = dict()
		path = "text"
		file_list = os.listdir(path)
		for filex in file_list:
			filex = path + '/' + filex
			f = open(filex)
			c = f.read()
			key = filex.split('/')[1].split('.')[0]
			numdict[key] = c
		return numdict

	# 拿到pc指数和移动指数
	def get_index(self, url):
		#~ js='window.open("%s");' % url
		#~ self.driver.execute_script(js)
		#~ handles = self.driver.window_handles
		#~ self.driver.switch_to.window(handles[len(handles) - 1])
		self.driver.get(url)
		self.driver.implicitly_wait(10)
		try:
			locator = (By.XPATH, '//div[@class="lrRadius"]/span[@class="ftlwhf enc2imgVal"]')
			WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
		except:
			return None, None
		time.sleep(3.5)
		e2 = self.driver.find_elements_by_css_selector("span[class='ftlwhf enc2imgVal']")
		lc1 = e2[0].location
		lc2 = e2[1].location

		filename = unquote(url.split('&word=')[1])
		self.driver.get_screenshot_as_file("screenshot/%s.png" % filename.decode('gbk'))
		im = Image.open("screenshot/%s.png" % filename.decode('gbk'))
		x1 = int(lc1['x'])
		y1 = int(lc1['y'])
		x2 = int(lc2['x'])
		y2 = int(lc2['y'])
		box1 = (x1, y1, x1 + 92, y1 + 19)
		region1 = im.crop(box1)
		box2 = (x2, y2, x2 + 92, y2 + 19)
		region2 = im.crop(box2)

		return region1, region2

	# 将图片对象分割成图片对象列表
	def splitimage(self,filee):
		region_list = list()
		width = filee.width
		height = filee.height
		i = width - 8
		while i > 8:
			box = (i, 0, i+8, height)
			region = filee.crop(box)
			i -= 8
			region_list.append(region)
		return region_list

	# 拿到数字
	def get_number(self, im):
		# 将图片对象转换为字符串
		text = self.image2text(im)
		if text in self.vals:
			i = self.vals.index(text)
			return self.keys[i]
		else:
			return None

	# 将图片对象转换成字符串
	def image2text(self, im):
		width = im.size[0]
		height = im.size[1]

		tmstr = ""
		for i in range(0,width):
			for j in range(0,height):
				cl=im.getpixel((i,j))
				clall = cl[0] + cl[1] + cl[2]
				if(clall==231):
					#黑色
					tmstr = tmstr + "1"
				else:
					tmstr = tmstr + "0"
			tmstr = tmstr + "\n"
		return tmstr

	def do_main(self):

		while not q.empty():
			try:
				tw = q.get()
				word = quote(tw)
				url = 'http://index.baidu.com/?tpl=trend&word=%s' % word

				pcindex, mobileindex = self.get_index(url)
				word = unquote(url.split('&word=')[-1])
				if pcindex != None and mobileindex != None:
					region_list1 = self.splitimage(pcindex)
					region_list2 = self.splitimage(mobileindex)
					nus1 = ""
					for r in region_list1:
						nu = self.get_number(r)
						if nu != None:
							nus1 = nus1 + nu

					nus2 = ""
					for r in region_list2:
						nu = self.get_number(r)
						if nu != None:
							nus2 = nus2 + nu
					txt = open(u'百度指数.txt', 'a')
					txt.write(word + ':' + str(nus1[::-1]) + ' ' + nus2[::-1] + '\n')
					txt.close()
					print tw.decode('gbk'), nus1[::-1], nus2[::-1]

				else:
					print tw.decode('gbk'), u"没有指数"
					txt = open(u'百度指数.txt', 'a')
					txt.write(word + ':' + 'No Index' + '\n')
					txt.close()
				log = open(u'log', 'a')
				log.write(word+',')
				log.close()
			except Exception as e:
				raise e
				continue


contents = open('words').read().split('\n')
if os.path.exists('log'):
	contentb = open('log').read().split(',')
else:
	contentb = list()
for con in contentb:
	if con in contents:
		contents.remove(con)
q = Queue.Queue()
for c in contents:
	q.put(c)


threads = list()
for i in xrange(5):
	a = BaiduIndex()
	t = Thread(target=a.do_main)
	threads.append(t)

# 启动所有线程
for thr in threads:
	thr.start()
