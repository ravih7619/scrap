from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
from datetime import date, datetime, timedelta
import MySQLdb
import re

sysDate = str(datetime.now())
print(sysDate)

'''db = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base
cur = db.cursor()'''

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="",  # your password
                     db="krishi_observ")  # name of the database
cur = db.cursor()

url = 'https://cssri.res.in/'
page = requests.get(url)
print(page)
checkCode = page.status_code
if checkCode == 200:
    tree = html.fromstring(page.content)
    currentData = tree.xpath('//td/text()')
    print("rough data: ", currentData)
    Data = (currentData[10], currentData[11], currentData[15], currentData[18], currentData[20], currentData[23])
    print("clean data: ", Data)
MaxTemp = currentData[10]
MinTemp = currentData[11]
RH = currentData[15]
WindSpeed = currentData[18]
Rainfall = currentData[20]
Evaporation = currentData[23]
D = tree.xpath('//tbody/tr/td/div/text()')
print("Date :", D)
d3 = re.findall(r"[\d]{1,2}.[\d]{1,2}.[\d]{4}", D[1])
a = d3[0]
date4 = datetime.datetime.strptime(a, '%d.%m.%Y').strftime('%Y-%m-%d')
print("Date: ", date4)

L = [MaxTemp, MinTemp, RH, WindSpeed, Rainfall, Evaporation, date4]
print(L)

result = None
try:
    q1 = "select * from cssri_weather_data where date='%s' ORDER by date, ID DESC " % (date4)
    print(q1)
    cur.execute(q1)
    result = cur.fetchall()
    print("Result: ", result)
    # conn.commit()
except (MySQLdb.Error, MySQLdb.Warning) as e:
    print("Error: ", e)

## Update Query Run on the basis of changes on all 4 data
try:
    ##update records if the record already exist in your table
    if result:
        q2 = "UPDATE cssri_weather_data SET MaxTemp='%s', MinTemp='%s', RH='%s', WindSpeed='%s', Rainfall='%s',Evaporation='%s' where date='%s' " % (
            MaxTemp, MinTemp, RH, WindSpeed, Rainfall, Evaporation, date4)
        print(q2)
        cur.execute(q2)

    else:
        q1 = "insert into cssri_weather_data (MaxTemp, MinTemp,  RH, WindSpeed ,Rainfall ,Evaporation,date, SystemDT) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            MaxTemp, MinTemp, RH, WindSpeed, Rainfall, Evaporation, date4, sysDate)
        print(q1)
        cur.execute(q1)
        db.commit()

except (MySQLdb.Error, MySQLdb.Warning) as e:
    print("Error: ", e)
db.close()
