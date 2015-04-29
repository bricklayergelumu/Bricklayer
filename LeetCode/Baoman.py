# -*- coding:utf8 -*-
from bs4 import BeautifulSoup
import os, sys, urllib2,time,random
path = os.getcwd()
new_path = os.path.join(path,'baozoumanhua')
if not os.path.isdir(new_path):
	os.mkdir(new_path)


def page_loop(page=1):
	url = 'http://baozoumanhua.com/all/hot/page/%s?sv=1389537379' % page
	content = urllib2.urlopen(url)
	soup = BeautifulSoup(content)

	my_girl = soup.find_all('div',class_='img-wrap')
	for girl in my_girl:
		jokes = girl.find('img')
		link = jokes.get('src')
		flink = link
		print flink
		content2 = urllib2.urlopen(flink).read()

		with open('baozoumanhua'+'/'+flink[-11:],'wb') as code:
			code.write(content2)

	page = int(page) + 1
	print 'Next Page'
	print 'the %s page' % page
	page_loop(page)
	
page_loop()

