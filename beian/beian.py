import requests
import os
from bs4 import BeautifulSoup
import sys
from style import Style, Fore, Back


'''

'''

class beiAn(object):
	
	def __init__(self, domain):
		
		self.domain = domain
		
		
	def params(self):
		
		print ('[+]' + Fore.GREEN + '配置参数中...' + Style.RESET_ALL)
		self.url = 'http://icp.chinaz.com/tbook.top'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.84 Safari/537.36',
		}
		print ('[+]' + Fore.GREEN + '正在获取[guid]参数...' + Style.RESET_ALL)
		resp = requests.get(self.url, headers=self.headers) # 获取guid
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '参数配置出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
			
		soup = BeautifulSoup(resp.text, 'html.parser')
		try:
			guid = soup.find_all('input', attrs={'name': 'guid'})[0]
			self.guid = guid['value']
			self.parameters = {
				'type': 'host',
				's': self.domain,
				'guid': self.guid,
				'code': '',
				'havecode': '0',
			}
		except Exception as e:
			print('[!]' + Fore.RED + '获取guid出现问题，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
			
			
	def request(self):
		
		print ('[+]' + Fore.GREEN + '发送请求中...' + Style.RESET_ALL)
		resp = requests.get(self.url, params=self.parameters, headers=self.headers)
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '请求出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
		self.result = resp.text
		
		
	def parser(self):
		
		print ('[+]' + Fore.GREEN + '解析中...' + Style.RESET_ALL)
		soup = BeautifulSoup(self.result, 'html.parser')
		try:
			result = soup.find_all('ul', attrs={'class': 'bor-t1s01', 'id': 'first'})[0]
			self.content = result.text
		except Exception as e:
			print('[!]' + Fore.RED + '解析出错，请稍后再试 :-(' + Style.RESET_ALL)
		
		
	def prettyPrint(self):
		
		print ('[+]' + Fore.GREEN + '结果：' + Style.RESET_ALL)
		print(Style.DIM + self.content
							.replace('主办单位名称', '主办单位名称: ')
							.replace('主办单位性质', '主办单位性质: ')
							.replace('网站备案/许可证号', '网站备案/许可证号: ')
							.replace('网站名称', '网站名称: ')
							.replace('网站首页网址', '网站首页网址: ')
							.replace('安全联盟(品牌宝)认证', '安全联盟(品牌宝)认证: ')
							.replace('审核时间', '\n审核时间: ')
							.replace('使用高级查询纠正信息', '')
							.replace('快捷查询 Whois查询 | SEO综合查询 | Alexa排名查询 | PR查询 | 网站测速 |  中文网站排名', '\n')
							+ Style.RESET_ALL)
		
	
	def main(self):
		
		self.params()
		self.request()
		self.parser()
		self.prettyPrint()
