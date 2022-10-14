import re
import MySQLdb
from lxml import html
import requests
import urllib
from bs4 import BeautifulSoup
import sys
import datetime

'''db = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base

cur = db.cursor()'''

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="",  # your password
                     db="krishi_observ")  # name of the data base
cur = db.cursor()

url = 'https://niasm.icar.gov.in/'
page = requests.get(url)
checkCode = page.status_code
print(checkCode)
if checkCode == 200:
    tree = html.fromstring(page.content)
    currentdata = tree.xpath('//td[@style="background-color:rgb(255, 255, 255)"]/text()')
    currentdata3 = tree.xpath('//h4/text()')
    currentdata4 = tree.xpath('//td[@style="background-color:rgb(255, 255, 255)"]/p/text()')
    print("CurrentData: ", currentdata, " : ", currentdata4, " : ", currentdata3)
#print(type(currentdata3))
MaxTemp = currentdata4[0]
MinTemp = currentdata[6]
RelativeHumidityMax = currentdata[8]
WindSpeed = currentdata[10]
PanEvaporation = currentdata[12]
Rainfall = currentdata[14]
d3 = re.findall(r"[\d]{1,2}.[\d]{1,2}.[\d]{4}", currentdata3[2])
a = d3[0]
#x3 = datetime.datetime.strptime('07.10.2022', '%d.%m.%Y').strftime('%Y-%m-%d')
x3 = datetime.datetime.strptime(a, '%d.%m.%Y').strftime('%Y-%m-%d')
print("Date: ", d3)
L = [MaxTemp, MinTemp, RelativeHumidityMax, WindSpeed, Rainfall, PanEvaporation, x3]
print(L)
sysDate = datetime.datetime.now()
result = None
try:
        q1 = "select * from niasm_weather_data where Date='%s' ORDER by Date, ID DESC " % (x3)
        print(q1)
        cur.execute(q1)
        result = cur.fetchall()
        print("Result: ", result)
        db.commit()
except (MySQLdb.Error, MySQLdb.Warning) as e:
        print("Error: ", e)

try:
        if (result):
            q2 = " UPDATE niasm_weather_data SET MaxTemp='%s',MinTemp='%s', MaxRelativeHumidity='%s',Windspeed='%s',Rainfall='%s',PanEvaporation='%s'  where Date='%s' " % (
                MaxTemp, MinTemp, RelativeHumidityMax, WindSpeed, Rainfall, PanEvaporation, x3)
            print(q2)
            cur.execute(q2)

        else:
            q1 = "insert into niasm_weather_data (MaxTemp,MinTemp,MaxRelativeHumidity,WindSpeed,Rainfall,PanEvaporation,Date, SystemDate) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                MaxTemp, MinTemp, RelativeHumidityMax, WindSpeed, Rainfall, PanEvaporation, x3, sysDate)
            print(q1)
            cur.execute(q1)

        db.commit()


except (MySQLdb.Error, MySQLdb.Warning) as e:

        print("Error: ", e)

db.close()
