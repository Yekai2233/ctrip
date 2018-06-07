import requests
from lxml import etree
import json
import re
import pymysql
import time

def parse_detial(name, room_id):
	headers = {
			"User-Agent": "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
			#"referer": "http://m.ctrip.com/webapp/Hotel/HotelDetail/346316.html",
			#"ccept" : "image/webp,image/apng,image/*,*/*;q=0.8",
			#"accept-encoding": "gzip, deflate, br",
			#"accept-language": "zh-CN,zh;q=0.9",
			#"Host": "m.ctrip.com",
			#"Upgrade-Insecure-Requests": "1",
			#"Connection": "keep-alive"
		}
		

	url = 'http://m.ctrip.com/webapp/Hotel/HotelDetail/'+ str(room_id) + '.html' 
	aspx = requests.post(url, headers=headers)

	#print(aspx.text)
	data = re.compile(r'__HOTEL_PAGE_DATA__\s=\s(.*?);\s*var', re.S).findall(aspx.text)[0]

	room_list = []

	json_data = json.loads(data)
	if json_data and 'roomlistinfo' in json_data.keys():
		for item in json_data['roomlistinfo']['rooms']:
			room = {}
			#print(item)
			
			room['time'] =  time.strftime("%Y-%m-%d %X", time.localtime())
			room['room_id'] = room_id
			if 'area' in item.keys():
				room['area'] = item['area']
				print(len(item['area']))
				print('2')
			else:
				room['area'] = 'area'
				print('1')
			#print(room['area'])
			if 'bed' in item.keys():
				room['bed'] = item['bed']
			else:
				room['bed'] = 'bed'
			#print(room['bed'])
			if 'bname' in item.keys():
				room['bname'] = item['bname']
			else:
				room['bname'] = 'bname'

			if 'floor' in item.keys():
				room['floor'] = item['floor']
			else:
				room['floor'] = 'floor'

			if 'maxNum' in item.keys():
				room['maxNum'] = item['maxNum']
			else:
				room['maxNum'] = 0

			if 'totalFinalFee' in item['priceInfo'].keys():
			#print(item['priceInfo']['totalFinalFee'].keys())
				room['price'] = item['priceInfo']['totalFinalFee']
			else:
				room['price'] = 0
				
				#print(room)
				#print('*'*40)
			room_list.append(room)
			
	return room_list


def main():
	db = pymysql.connect(
			    user='root',
			    password='qwer',
			    host='127.0.0.1',
			    port= 3306,
			    database='fangjia',
			    use_unicode=True, 
			    charset="utf8"
			)

	cursor = db.cursor()
	cursor.execute("select room_id from ctriphangzhou")
	

	room_id_list = cursor.fetchall()
	a = 0			
	for id in room_id_list:
		a += 1
		name = 'hangzhou' + str(id[0])
		room_id = id[0]
		print(name)
		print(a)

		#print(id[0])
		detail_list = parse_detial(name, room_id)
		time.sleep(2)
		#print(detail_list)
		for i in detail_list:
			#print(type(i['time']))
			print("INSERT ignore INTO %s(room_id, area, bed, bname, floor, maxNum, price, time) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s, '%s')" %(name, i['room_id'], i['area'], i['bed'], i['bname'], i['floor'], i['maxNum'], i['price'], i['time']))
			cursor.execute("INSERT ignore INTO %s(room_id, area, bed, bname, floor, maxnum, price, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s, '%s')" %(name, i['room_id'], i['area'], i['bed'], i['bname'], i['floor'], i['maxNum'], i['price'], (i['time'])))
			db.commit()
	#print(room_list)
	print(a)
	db.commit()
	cursor.close()	

if __name__ == '__main__':
	main()





'''print(aspx.status_code)
print(url)
html = etree.HTML(aspx.text)
result1 = html.xpath('//div[@class="cell-star room-column  room--space" or @class="cell-star dl-cell  room--space"]')
#result2 = html.xpath('//div[@class="cell-star dl-cell  room--space"]')

#result = result1 + result2
#print(result[0].xpath('./div')[0].text.encode('utf-8'))
print(len(result1))
#print(len(result1),len(result2),len(result))
#print(result[4].text)

	#f.write(result1[1].text)

for i in result1:
	
	h = i.xpath('./div/h3')[0].text
	detial = i.xpath('./div/p[@class="room-size"]')[0].xpath('string(.)')
	print(h,detial)'''
		#f.write(h)	
	
#for i in range(len(result)):