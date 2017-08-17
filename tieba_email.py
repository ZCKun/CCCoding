import requests
import re
import sys
import pymysql


class tiebaEmail(object):
	
	def __init__(self, posts_id):
		
		self.tmp_url = 'http://tieba.baidu.com/p/{}?pn=1'.format(posts_id)
		self.urls = None
		self.id = posts_id
		self.reg = re.compile('[0-9a-zA-Z\-_]{2,15}@[0-9a-zA-Z]{2,10}\.[0-9a-zA-Z]{2,5}')
		self.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.84 Safari/537.36",
		}
		self.build()
		
		
	def build(self):
		
		resp = requests.get(self.tmp_url, headers=self.headers)
		if resp.status_code != requests.codes.OK:
			print('Request Error ):')
			sys.exit()
		try:	
			page = int(re.findall('共<span class="red">(.*?)</span>页', resp.text, re.S)[0])
			print(page)
		except Exception as e:
			print("Error:", e)
			sys.exit()
		
		_ = 'http://tieba.baidu.com/p/%s?pn={}'% self.id
		self.urls = [ _.format(pn) for pn in range(1,page+1) ]
		

	def request(self):
		
		results = []
		
		for url in self.urls:
			resp = requests.get(url, headers=self.headers)
			if resp.status_code != requests.codes.OK:
				print("request error ):")
				continue
			results.append(resp.text)
			
		return results
		
		
	def parser(self):
		
		self.content = []
		for result in self.request():
			for i in self.reg.findall(result, re.S):
				self.content.append(i.lowser())
				

	def prettyPrint(self):
		
		print(len(self.content))
		#for i in self.content:
			#print("INSERT INTO email VALUES ({})".format(i))


	def connection_mysql(self):
		
		db = pymysql.connect("192.168.1.101", "zckun", "zckuna", "Public")
		cursor = db.cursor()
		for i in self.content:
			try:
				cursor.execute('INSERT INTO email VALUES ("{}")'.format(i))
			except Exception as e:
				print("\033[1;31mERROR\033[0m: \033[0;31m%s\033[0m ):"% e)
				continue
		db.commit()
		cursor.close()
		db.close()
		print("DONE! (:")
		
		
if __name__ == '__main__':
	email = tiebaEmail('5178628955')
	email.parser()
	#email.prettyPrint()
	email.connection_mysql()
