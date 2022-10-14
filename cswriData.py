import re
import MySQLdb
import bs4
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
def _itersplit(l, splitters):
    current = []
    for item in l:
        if item in splitters:
            yield current
            current = []
        else:
            current.append(item)
    yield current


def magicsplit(l, *splitters):
    return [subl for subl in _itersplit(l, splitters) if subl]


res = requests.get('http://www.cswri.res.in/')
soup = bs4.BeautifulSoup(res.text, 'lxml')
soup.select("title")
soup.select(".title")
A = []
for name in soup.select(".title"):
    A.append(name.text)
a = A[8]

ab = str(a.replace('Weather on ', ''))
print(ab)
time = datetime.date.today()
sysDate = datetime.datetime.now()
# print (sysDate, time)
compareDate = datetime.datetime.strptime(str(ab), '%d %b,%Y').strftime('%Y-%m-%d')
# print ("CompareDate: ",compareDate)
# d1 = re.findall(r'\d{2}.\w{3,}.\d{4}', A[8])
# print(d1)
x2 = compareDate

soup.select("table")
B = []
for val in soup.select("table"):
    B.append(val.text)
b = B[5]
# print(b)
c = b.split()
# print(c)
C = magicsplit(c, 'Temperature', 'Max.', 'Min.', '(0c)', 'R.H.(%)', 'Wind', 'Velocity', 'Rainfall', 'Evaporation')
# print(C)
for val in C[0]:
    val0 = val.split(')')
for val in C[1]:
    val1 = val.split(')')
for val in C[2]:
    val2 = val.split('.', 1)
for val in C[3]:
    val3 = val.split(')')
for val in C[4]:
    val4 = val.split(')')
for val in C[5]:
    val5 = val.split(')')

value_list = [val0[1], val1[1], val2[1], val3[1], val4[1], val5[1]]
print("************",value_list)
MaxTemp = val0[1]
MinTemp = val1[1]
RF = val4[1]
RH = val2[1]
WS = val3[1]
EVP = val5[1]

result = None
try:
    q1 = "select * from cswri_weather_data where date='%s' ORDER by date, ID DESC " % (x2)
    # print (q1)
    cur.execute(q1)
    result = cur.fetchall()
except Exception as e:
    # print ("E1: ")
    print(str(e))

try:
    ##update records if the record already exist in your table
    if (result):
        q2 = "UPDATE cswri_weather_data SET MaxTemp='%s',MinTemp='%s',Rainfall='%s', RH='%s', WS='%s', EVP='%s' where date='%s' " % (
        MaxTemp, MinTemp, RF, RH, WS, EVP, x2)
        print(q2)
        cur.execute(q2)

    else:
        q1 = "insert into cswri_weather_data (MaxTemp, MinTemp, Rainfall, RH, ws, evp, date, SystemDT) values ('%s','%s','%s','%s','%s','%s','%s','%s') " % (
        MaxTemp, MinTemp, RF, RH, WS, EVP, x2, sysDate)
        print(q1)
        cur.execute(q1)
    db.commit()
except Exception as e:
    # print ("E1: ")
    print(str(e))
db.close()
