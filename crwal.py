from bs4 import BeautifulSoup
import requests
import csv

url = 'http://hz.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000'

#初始化page=0
page = 0

with open('rent_beijing.csv','w',encoding='utf-8', newline='') as fp:
	csv_writer = csv.writer(fp,delimiter=',')
	
	while True:
		page += 1
		print('fetch:',url.format(page=page))
		response = requests.get(url.format(page=page))
		html = BeautifulSoup(response.text,'lxml')
		house_list = html.select('.list > li')
		#读不到新的房源时结束
		if not house_list:
			break
		
		for house in house_list:
			house_title = house.select('h2')[0].string
			house_url = 'http://hz.58.com/%s'%(house.select('a')[0]['href'])
			house_info_list = house_title.split()

			#
			if '公寓'in house_info_list[1] or '青年社区' in house_info_list[1]:
				house_location = house_info_list[1]
			else:
				house_location = house_info_list[1]
			
			house_money = house.select('.money')[0].select('b')[0].string
				# print([house_title,house_location,house_money,house_url])
			csv_writer.writerow([house_title,house_location,house_money,house_url])

# 启动服务  python -m http.server 3000
# 登录localhost:3000