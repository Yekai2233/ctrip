import pymysql

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
a = 0
room_id = cursor.fetchall()
for i in room_id:
	a += 1
	name = 'hangzhou' + str(i[0])
	print(name)
	print(a)
	cursor.execute("create table %s (id int auto_increment primary key, time DATETIME, room_id varchar(20), area varchar(20), bed varchar(20), bname varchar(20), floor varchar(20), maxnum int, price int,foreign key(room_id) references ctriphangzhou(room_id))" %name)
print(a)
db.commit()
cursor.close()