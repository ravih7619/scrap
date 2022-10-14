from DateTime import DateTime
from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
import datetime
from datetime import timedelta
import MySQLdb
import re
from datetime import date, timedelta
#import matplot
import dateutil.parser as dparser
import numpy

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="",  # your password
                     db="krishi_observ")  # name of the database

cur = db.cursor()
'''db = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base

cur = db.cursor()'''


## For find index of Date in Bold <b> html tag
# https://stackoverflow.com/questions/3276180/extracting-date-from-a-string-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
def findIndex(lst, a):
    result = []
    for i, x in enumerate(lst):
        # if x == a :
        # if a in x :
        if dparser.parse(x, fuzzy=True) != '':
            result.append(i)
    return result


##Generate System Date
time = datetime.date.today()
sysDate = datetime.datetime.now()

print(sysDate, time)
compareDate = datetime.datetime.strptime(str(time), '%Y-%m-%d').strftime('%d-%m-%Y')
print("CompareDate: ", compareDate)
# d = datetime.datetime.strptime(orig_date, '%Y-%m-%d %H:%M:%S')
# d = d.strftime('%m/%d/%y')

for i in range(20):
    # url='http://localhost/ccari.html'
    url = 'https://ccari.icar.gov.in'
    page = requests.get(url)
    # v print (page)

#### Check url if exist
# checkNull = page.text
checkCode = page.status_code
# print checkCode
if checkCode == 200:
    tree = html.fromstring(page.content)

    # MaxTemp=tree.xpath('//span[@style="font-size: 12.0pt; font-family: \'Times New Roman\',serif; color: #008000"]/text()')
    # Data=tree.xpath('//span[@style="font-size: 12.0pt; font-family: \'Times New Roman\',serif; color: green"]/text()')
    WhetherData = tree.xpath('//span[@class="c39"]/text()')
    '''WhetherData1 = tree.xpath('//p[@class="c3"]/text()')
    WhetherData2 = tree.xpath('//span[@class="c7"]/text()')
    date=tree.xpath('//span[@class="c4"]/text()')

    print ("WData: ", WhetherData)

    print ("WData: ", WhetherData[0])
    print ("WData1: ", WhetherData[1])
    print ("WData2: ", WhetherData[3])
    print ("WData3: ", WhetherData[4])
    print ("WData4: ", WhetherData[5])
    print ("WData5: ", WhetherData[6])
    print ("WData6: ", WhetherData[7])
    print ("WData7: ", WhetherData[8])
    print ("WData8: ", WhetherData[9])
    print ("WData9: ", WhetherData[10])'''
    print("WData10: ", WhetherData[11])
    print("WData11: (MaxTemp)", WhetherData[12])
    print("WData12: ", WhetherData[13])
    print("WData13: ", WhetherData[14])
    print("WData14: ", WhetherData[15])

    # L=[WhetherData[11],WhetherData[12],WhetherData[13],WhetherData[14],WhetherData[15]]
    # print L

    d1 = ""
    # d1 = re.findall(r'\d{1}-\d{2}-\d{4}', WhetherData[11])
    # d1 = re.findall(r'\d{2}-\d{2}-\d{4}', WhetherData[11])
    # print "Date: ", d1[0]

    if (re.findall(r'\d{1}-\d{2}-\d{4}', WhetherData[11])):
        d11 = re.findall(r'\d{1}-\d{2}-\d{4}', WhetherData[11])
        d1 = "0" + d11[0]
        print("D: " + d1)
    if (re.findall(r'\d{2}-\d{1}-\d{4}', WhetherData[11])):
        d11 = re.findall(r'\d{2}-\d{1}-\d{4}', WhetherData[11])
        d12 = d11[0].split("-")
        d1 = d12[0] + "-0" + d12[1] + "-" + d12[2]
        print("d12: " + d1)
    if (re.findall(r'\d{1}-\d{1}-\d{4}', WhetherData[11])):
        d11 = re.findall(r'\d{1}-\d{1}-\d{4}', WhetherData[11])
        d12 = d11[0].split("-")
        d1 = "0" + d12[0] + "-0" + d12[1] + "-" + d12[2]
        print("d13: " + d1)
    if (re.findall(r'\d{2}-\d{2}-\d{4}', WhetherData[11])):
        d1 = re.findall(r'\d{2}-\d{2}-\d{4}', WhetherData[11])
        d1 = d1[0]
        print("d14: " + d1)

    d2 = re.findall(r'\d{2}.\d{1}', WhetherData[11])
    if len(d2) == 0:
        d2 = re.findall(r'\d{2}.\d{1}', WhetherData[11])
    if len(d2) == 0:
        d2 = re.findall(r'\d{2}.\d{1}', WhetherData[11])
    print("MaxTemp: ", d2[0])

    d3 = re.findall(r'\d{3}.\d{1}', WhetherData[12])
    if len(d3) == 0:
        d3 = re.findall(r'\d{2}.\d{1}', WhetherData[12])
    if len(d3) == 0:
        d3 = re.findall(r'\d{1}.\d{1}', WhetherData[12])
    print("MinTemp: ", d3[0])

    d4 = re.findall(r'\d{3}', WhetherData[13])
    if len(d4) == 0:
        d4 = re.findall(r'\d{2}', WhetherData[13])
    if len(d4) == 0:
        d4 = re.findall(r'\d{1}', WhetherData[13])
    print("Rainfall: ", d4[0])

    d5 = re.findall(r'\d{3}', WhetherData[14])
    if len(d5) == 0:
        d5 = re.findall(r'\d{2}', WhetherData[14])
    if len(d5) == 0:
        d5 = re.findall(r'\d{1}', WhetherData[14])
    print("Humidity: ", d5[0])

    # yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    # x2= datetime.datetime.strptime(yesterday, '%d-%m-%Y').strftime('%Y-%m-%d')
    x2 = date.today().strftime('%Y-%m-%d')
    # x2 = (date3 - timedelta(days=1)).strftime('%Y-%m-%d')
    # print "yesterday: ", x2, " Date3: ", date3

    MaxTemp = d2[0]
    MinTemp = d3[0]
    Rainfall = d4[0]
    RH = d5[0]
    # date=d1[0]
    date = d1

    result = None
    try:
        q1 = "select * from ccari_weather_data where date='%s' ORDER by date, ID DESC " % (x2)
        print(q1)
        cur.execute(q1)
        result = cur.fetchall()
        print("Result: ", result, " One:", result[0][1])
        db.commit()
    except:

        ## Update Query Run on the basis of changes on all 4 data
        try:
            ##update records if the record already exist in your table
            if (result):
                q2 = "UPDATE ccari_weather_data SET MaxTemp='%s',MinTemp='%s',Rainfall='%s', RH='%s' where date='%s' " % (
                    MaxTemp, MinTemp, Rainfall, RH, x2)
                print(q2)
                if (result[0][1] == MaxTemp and result[0][2] == MinTemp and result[0][3] == Rainfall and result[0][
                    4] == RH):
                    cur.execute(q2)

            else:
                q1 = "insert into ccari_weather_data (MaxTemp, MinTemp, Rainfall, RH, date) values ('%s','%s','%s','%s','%s')" % (
                    MaxTemp, MinTemp, Rainfall, RH, x2)
                print(q1)
                cur.execute(q1)

            db.commit()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print("Error: ", e)

db.close()
