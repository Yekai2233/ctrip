#coding=utf8
import requests
from lxml import etree
import json
import re
import pymysql
import time


#初始URL 获得携程链接
start_url = "http://hotels.ctrip.com/hotel/hangzhou17#ctm_ref=ctr_hp_sb_lst"


def first_spider(start_url):
	headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'Host': 'hotels.ctrip.com',
			'Origin':'http://hotels.ctrip.com',			
		}

	#获得第一次响应，记录formdata需要的数据
	response = requests.get(url=start_url, headers=headers)
	result_html = response.text
	#print(result_html)

	html = etree.HTML(result_html)
	
	#三个formdata数据
	page = int(html.xpath('//input[@class="c_page_num"]/@data-pagecount')[0]) + 1
	result = html.xpath('//div[@class="hotel_new_list"]/@id')
	hotalid = []	
	for i in result:
		id = str(i) + '_' + str(result.index(i)+1) + '_' + '1'
		hotalid.append(id)

	#开始循环获取
	for p in range(1,page):
		#爬取列表
		aspx = spider(result, hotalid, p)
		#解析并存数列表的数据
		parse(aspx,p)
		time.sleep(2)
		

def retry(func):
    def retried_func(*args, **kwargs):
        MAX_TRIES = 3
        tries = 0
        while True:
            resp = func(*args, **kwargs)
            if resp == 1 and tries < MAX_TRIES:
                print("尝试中")
                tries += 1
                continue
            break
        return resp
    return retried_func


#爬取aspx连接
#有时获取到的页面会出错，用此方式来重新获取响应	
@retry
def spider(result, hotalid, p):
	

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Host': 'hotels.ctrip.com',
		'Origin':'http://hotels.ctrip.com',	
		'Referer':'http://hotels.ctrip.com/hotel/hangzhou17'	
	}
	formdata = {
		'__VIEWSTATEGENERATOR':'DB1FBB6D',
		'cityName':'%E6%9D%AD%E5%B7%9E',
		#'StartTime':'2018-05-01',
		#'DepTime':'2018-05-02',
		'RoomGuestCount':'1,1,0',
		'operationtype':'NEWHOTELORDER',
		'IsOnlyAirHotel':'F',
		'cityId':'17',
		'cityPY':'hangzhou',
		'cityCode':'0571',
		'cityLat':'30.2799952044',
		'cityLng':'120.1616127798',
		'htlPageView':'0',
		'hotelType':'F',
		'hasPKGHotel':'F',
		'requestTravelMoney':'F',
		'isusergiftcard':'F',
		'useFG':'F',
		'priceRange':'-2',
		'promotion':'F',
		'prepay':'F',
		'IsCanReserve':'F',
		'OrderBy':'99',
		'checkIn':'2018-05-01',
		'checkOut':'2018-05-02',
		'hidTestLat':'0%7C0',
		'AllHotelIds': result,
		'HideIsNoneLogin':'T',
		'isfromlist':'T',
		'ubt_price_key':'htl_search_result_promotion',
		'isHuaZhu':'False',
		'htlFrom':'hotellist',
		'hotelIds': hotalid,
		'markType':'0',
		'a':'0',
		'contrast':'0',
		'contyped':'0',
		'page': p,
		}

	url2 = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
	aspx = requests.post(url2, data=formdata, headers=headers).text

	try:
		data = json.loads(aspx)
	except:
		return 1	
	else:
		return data
		
	
	

#json数据解析
def parse(data,p):	
	try:
		if data != 1:

			if data and 'hotelPositionJSON' in data.keys():
				for item in data.get('hotelPositionJSON'):
					
					name = item['name']
					lat = item['lat']
					lon = item['lon']
					address = item['address']
					quyu = item['address'][:3]
					url = 'http://hotels.ctrip.com/' + item['url']
					city = "杭州"
					citycode = 17
					room_id = item['id']
					print(house_id)
					save_to_mysql(name, lat, lon, address, quyu, url, city, citycode, room_id)
		else:
			print('获取的页面无法用json解析')
	except Exception as e:
		print(e)
		pass
			
		

#存入mysql
def save_to_mysql(name, lat, lon, address, quyu, url, city, citycode,room_id):
	try:	
		
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
		cursor.execute("INSERT ignore INTO ctriphangzhou(name, lat, lon, address, quyu, url, city, citycode, room_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" ,(name, lat, lon, address, quyu, url, city, citycode,house_id))
		db.commit()
		cursor.close()
	except Exception as e:
		print(e + '插入出错')
		pass

first_spider(start_url)















'''id = 9
city = "hangzhou"
citycode = 17
house_id = 1245
name = '杭州马可波罗假日酒店'
lat = 12.36
lon = 23.63
address = '上车去看了看少得可怜萨达姆可能呢'
quyu = '是对的'
url = 'http://hotels.ctrip.com/'
'''
#cursor.execute("INSERT INTO ctriphangzhou(house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8})" .format(house_id, name, lat, lon, address, quyu, url1, city, citycode))
#cursor.execute("INSERT INTO ctriphangzhou(id,house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" ,(id, house_id, name, lat, lon, address, quyu, url1, city, citycode))
#cursor.execute("select * form ctriphangzhou")
'''a = "INSERT INTO ctriphangzhou(house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8})" ,(house_id, name, lat, lon, address, quyu, url1, city, citycode)
b = "INSERT INTO ctriphangzhou(house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES ('1', 'na', '21.51153', '92.8835', 'a', 'qu', 'urs', 'csj', '37')" 
c = 'insert into lcj(name,age) vaules(%s,%s)',('ff',18)
print(a,b,c)'''
'''sql3 = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%s', '%s', '%s' )" 
      
sql2 = """INSERT INTO ctriphangzhou(id,house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES (id, house_id, name, lat, lon, aess, quyu, url, city, citycode)"""
		

cursor.execute(sql3,(house_id, name, lat, lon, address))'''
#sql_insert ="INSERT INTO ctriphangzhou(house_id,name,lat,lon,address,quyu,url,city,citycode）VALUES (1, 'name', 1.555553, 2.8835, 'address', 'quyu', 'url', 'city', 17 )" 

'''cursor.execute('select * from ctriphangzhou')  ##具体的数据库操作语句  
        data=cursor.fetchall()
        print(data)'''        
#cursor.execute(sql_insert) 

#first_spider(start_url)
'''db = pymysql.connect(
	    user='root',
	    password='qwer',
	    host='127.0.0.1',
	    port= 3306,
	    database='fangjia',
	    use_unicode=True, 
	    charset="utf8"
	)

cursor = db.cursor() 
cursor.execute('SET NAMES utf8;') 
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')'''
#cursor.execute("INSERT INTO ctriphangzhou(id,house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" ,(id, house_id, name, lat, lon, address, quyu, url, city, citycode))
#db.commit()
#cursor.close()

#INSERT INTO ctriphangzhou(house_id,name,lat,lon,address,quyu,url,city,citycode) VALUES (1, 'name', 1.233, 2.635, 'address', 'quyu', 'url', 'city', 17),[1, 'name', 1.233, 2.635, 'address', 'quyu', 'url', 'city', 17]