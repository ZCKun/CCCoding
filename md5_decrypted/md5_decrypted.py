import requests
import re
from bs4 import BeautifulSoup
import os
import sys
import argparse
from style import Style, Fore, Back


'''
采用网站：http://www.dmd5.com/
思路：
	因为提交解密请求需要三个参数，首先获取参数：
		1、第一个参数 [_VIEWRESOURSE] 固定值 [c4c92e61011684fc23405bfd5ebc2b31]
		2、第二个参数 [md5] 也就是我们要解密的密文
		3、第三个参数 [result] 这个参数必须通过POST
			[http://www.dmd5.com/md5Util.jsp?method=crack&type=1&md5=[密文]]
			POST参数 :
				{
					'md5': '密文', 
					'method': 'crack', 
					'type': '1'
				}
			该地址来获取
		4、请求http://www.dmd5.com/md5-decrypter.jsp解密
			POST参数：
				{
					'_VIEWRESOURSE': 'c4c92e61011684fc23405bfd5ebc2b31',
					'md5': '密文',
					'result': result
				}

'''

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
	
		data = {
			'_VIEWRESOURSE': 'c4c92e61011684fc23405bfd5ebc2b31',
			'md5': self.md5,
			'result': self.result
		}
		
		print ('[+]' + Fore.GREEN + '发送请求中...' + Style.RESET_ALL)
		resp = self.session.post(self.urls.get('crack'), data=data, headers=self.headers)
		if resp.status_code != requests.codes.OK:
			print('[!]' + Fore.RED + '请求出错，请稍后再试 :-(' + Style.RESET_ALL)
			sys.exit()
			
		self.content = resp.text


	def parser(self):
		
		print ('[+]' + Fore.GREEN + '解析中...' + Style.RESET_ALL)
		soup = BeautifulSoup(self.content, 'html.parser')

		try:
			'''<div class="alert alert-info" style='width: 75%; margin: 0 auto; margin-top: -60px' role="alert">'''
			alert = soup.find_all('div', attrs={'class': 'alert alert-info'})[1]
			self.result = [_.text for _ in alert.find_all('p')]
		except Exception as e:
			print('[!]' + Fore.RED + '解析出错，请稍后再试 :-(' + Style.RESET_ALL)
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
	
		md5 = sys.argv[1]
		md = md5Decrypted(md5)
		md.main()
