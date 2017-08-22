# encoding: utf-8

import sys
import requests
import re
from bs4 import BeautifulSoup
import logging
from style import Style, Fore, Back


class whoIs(object):
	
	def __init__(self, domian):
		''' init '''
		
		self.url = 'http://whois.chinaz.com/'
		self.parameters = {
			'DomainName': domian,
			'ws': 'whois.nic.top',
		}
		self.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.84 Safari/537.36",
		}
		
		self.request()
		
		
	def request(self):
		''' request aims web page '''
		
		print ('[+]' + Fore.GREEN + '开始请求...' + Style.RESET_ALL)
		resp = requests.get(self.url, headers=self.headers, params=self.parameters)
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '请求出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
		self.content = resp.text
	

	def parser(self):
		''' parse content '''
		
		print ('[+]' + Fore.GREEN + '开始解析...' + Style.RESET_ALL)
		wsSoup = BeautifulSoup(self.content, 'html.parser')
		
		self.clearfix_bor_b1s = wsSoup.find_all(attrs={
			'class': 'clearfix bor-b1s '
		})
		self.clearfix_bor_b1s_bg_list = wsSoup.find_all(attrs={
			'class': 'clearfix bor-b1s bg-list'
		})
		


	def prettyPrint(self):
		
		self.parser()
		print('[+]' + Style.DIM + '结果: \n' + Style.RESET_ALL)
		for _,__ in zip(self.clearfix_bor_b1s, self.clearfix_bor_b1s_bg_list):
			print(_.text)
			print(__.text.replace('[whois反查]', ''))
		
		

if __name__ == '__main__':
	
	domain = sys.argv[1]
	ws = whoIs(domain)
	ws.prettyPrint()
		
		
		
		
