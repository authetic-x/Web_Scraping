# coding: utf8

import pymysql

'''
db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print('Database version:', data)
cursor.execute('CREATE DATABASE spiders DEFAULT CHARACTER SET utf8')
db.close()
'''

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, ' \
      'name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
cursor.execute(sql)

id = '2016211072'
user = 'Bob'
age = 20

sql1 = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'
try:
    cursor.execute(sql1, (id, user, age))
    print('Successful!')
    db.commit()
except:
    print('Failed!')
    db.rollback()

db.close()
