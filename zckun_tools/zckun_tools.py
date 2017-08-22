#encoding: utf-8

__author__ = "zckun"

import requests
import os
from bs4 import BeautifulSoup
import sys
from style import Style, Fore, Back
import argparse


'''
集合工具，会更新
'''

class beiAn(object):
	
	def __init__(self, domain):
		
		self.domain = domain
		self.params()
		
		
	def params(self):
		'''设置／获取一些请求必要的参数'''
		
		print ('[+]' + Fore.GREEN + '配置参数中...' + Style.RESET_ALL)
		self.url = 'http://icp.chinaz.com/{}'.format(self.domain)
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
							.replace('查看截图', '')
							.strip()
							+ Style.RESET_ALL)
		
	
	def main(self):
		
		self.request()
		self.parser()
		self.prettyPrint()
		
# Whois查询
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
		self.whoisLeft = wsSoup.find_all('ul', attrs={
			'class': 'WhoisLeft fl'
		})[0]


	def prettyPrint(self):
		
		print('[+]' + Fore.GREEN + '结果: \n' + Style.RESET_ALL)
		print(Style.DIM + self.whoisLeft.text
							.replace('\n', '')
							.replace('[whois反查]', '')
							.replace('whois反查', '')
							.replace('注册商', '\n注册商: ')
							.replace('联系人', '\n联系人: ')
							.replace('联系邮箱', '\n联系邮箱: ')
							.replace('联系电话', '\n联系电话: ')
							.replace('更新时间', '\n更新时间: ')
							.replace('创建时间', '\n创建时间: ')
							.replace('过期时间', '\n过期时间: ')
							.replace('公司', '\n公司: ')
							.replace('域名服务器', '\n域名服务器: ')
							.replace('DNS', '\nDNS: ')
							.replace('状态域名', '\n状态域名')
							.replace('-------站长之家', '\n-------ZCKUNA ')
							#.replace('域名', '\n域名: ')
							.replace(' ','')
							.replace('[whois反查]其他常用域名后缀查询：cncomccnetorg', '')
							.strip()
							+ Style.RESET_ALL)
		
		
	def main(self):
		
		self.parser()
		self.prettyPrint()
		
		
# MD5解密
class md5Decrypted(object):
	
	def __init__(self, md5):
		
		self.md5 = md5
		self.session = requests.Session()
		self.params()
		
		
	def params(self):
		
		print ('[+]' + Fore.GREEN + '配置参数中...' + Style.RESET_ALL)
		self.urls = {
			'crack': 'http://www.dmd5.com/md5-decrypter.jsp',
			'result': 'http://www.dmd5.com/md5Util.jsp',
		} 
		
		params = {
			'method': 'crack',
			'type': '1',
			'md5': self.md5
		}
		
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.84 Safari/537.36',
		}
		
		data = {
			'method': 'crack',
			'type': '1',
			'md5': self.md5
		}
		
		resp = self.session.post(self.urls.get('result'), params=params, data=data, headers=self.headers) # 获取参数result的post
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '参数配置出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()

		self.result = resp.text.strip()


	def request(self):
		'''这里提示［分析中］其实是为了装X...'''
		
		data = {
			'_VIEWRESOURSE': 'c4c92e61011684fc23405bfd5ebc2b31',
			'md5': self.md5,
			'result': self.result
		}
		
		print ('[+]' + Fore.GREEN + '分析中...' + Style.RESET_ALL)
		resp = self.session.post(self.urls.get('crack'), data=data, headers=self.headers)
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '分析出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
			
		self.content = resp.text


	def parser(self):
		
		print ('[+]' + Fore.GREEN + '解密中...' + Style.RESET_ALL)
		soup = BeautifulSoup(self.content, 'html.parser')

		try:
			'''<div class="alert alert-info" style='width: 75%; margin: 0 auto; margin-top: -60px' role="alert">'''
			alert = soup.find_all('div', attrs={'class': 'alert alert-info'})[1]
			self.result = [_.text for _ in alert.find_all('p')]
		except Exception as e:
			print('[!]' + Fore.RED + '解密出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
		
		
	def prettyPrint(self):
		
		print ('[+]' + Fore.GREEN + '结果：\n ' + Style.RESET_ALL)
		for _ in self.result:
			print(Style.DIM + _ + Style.RESET_ALL)
		
	
	def main(self):
		
		self.request()
		self.parser()
		self.prettyPrint()

		
	
if __name__ == '__main__':
	
	global domain
	# domain = sys.argv[1]
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-d", "--domain")
	
	params = parser.parse_args()
	domain = params.domain
	
	print(Fore.LIGHTBLUE_EX + '快捷查询: [0]退出 | [1]Whois查询 | [2]备案查询 | [3]设置域名 | [4]md5解密' + Style.RESET_ALL)
	while True:
		if domain == '' or domain is None:
			print('[' + Fore.LIGHTYELLOW_EX + '!' + Style.RESET_ALL + ']' + Fore.LIGHTYELLOW_EX + '提示: 您当前未设置域名' + Style.RESET_ALL)
		select = input('[?]>> ')
		if select == '1':
			if domain == '' or domain is None:
				print('[' + Fore.LIGHTYELLOW_EX + '!' + ']' + Fore.RED + '请先设置域名 :)' + Style.RESET_ALL)
				while True:
					domain = input('[' + Fore.GREEN + '域名' + Style.RESET_ALL + ']>> ')
					if domain != '':
						break
			ws = whoIs(domain)
			ws.main()
		elif select == '2':
			if domain == '' or domain is None:
				print('[' + Fore.LIGHTYELLOW_EX + '!' + ']' + Fore.RED + '请先设置域名 :)' + Style.RESET_ALL)
				while True:
					domain = input('[' + Fore.GREEN + '域名' + Style.RESET_ALL + ']>> ')
					if domain != '':
						break
			ba = beiAn(domain)
			ba.main()
		elif select == '3':
			while True:
					domain = input('[' + Fore.GREEN + '域名' + Style.RESET_ALL + ']>> ')
					if domain != '':
						break
			print(Fore.LIGHTBLUE_EX + '快捷查询: [0]退出 | [1]Whois查询 | [2]备案查询 | [3]设置域名 | [4]md5解密' + Style.RESET_ALL)
		elif select == '4':
			ciphertext = input('[' + Fore.GREEN + '密文' + Style.RESET_ALL + ']>> ')
			md = md5Decrypted(ciphertext)
			md.main()
		elif select == '0':
			sys.exit()
		
	
	
