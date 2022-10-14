from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
from datetime import date, datetime, timedelta
import MySQLdb
import re
import datetime

'''db = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base

cur = db.cursor()'''

conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="krishi_observ")  # Local Configuration
x = conn.cursor()


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


##url of the organisation whose data has to scarp.
url = 'https://crijaf.icar.gov.in/SideLinks/QuickLinks/AgrometeorologicalData.php'

page = requests.get(url)
#### Check url if exist
checkNull = page.text
checkCode = page.status_code
# print checkCode
if checkNull != "" and checkCode == 200:
    tree = html.fromstring(page.content)
    CurrentData = tree.xpath('//td/text()')
B = magicsplit(CurrentData, '\r\n')
# print(B)
D = B[0]
E = D[3:len(B[0])]
# Replace 16(old site) to 10(new site)
C = [E[i:i + 10] for i in range(0, len(E), 10)]
# print(C)
length = (len(D[0]) // 10)
print("After: ", B[0])
F = (int(len(D) // 10))

for i in range(int(F - 1)):
    j = i
    x1 = C[length - j][1]
    x2 = x1.split('-')
    # print("X1-X2: ", x1, x2)
    x20 = x2[0]
    x21 = re.findall(r'\d{2}.\d{2}.\d{4}', x2[1])
    x22 = ' '.join(x21)
    x3 = datetime.datetime.strptime(str(x20), '%d/%m/%Y').strftime('%Y-%m-%d')
    x4 = datetime.datetime.strptime(str(x22), '%d/%m/%Y').strftime('%Y-%m-%d')
    print(x3, x4)

    result = None
    checkString = ""
    try:
        checkString = float(C[length - j][7])
    except(ValueError) as e:
        checkString = "'" + C[length - j][7] + "'"
    # print checkString
    try:
        q1 = "select * from crijafData where grp_days='%s'" % (C[length - j][1])
        print("Q1: ", q1)
        x.execute(q1)
        result = x.fetchall()
        print("Result: " + result)
        conn.commit()
    except:
        conn.rollback
        No_data = None
        BL = "'-'"  # use for NAN data aas in SOIL Temperature data now remove from source
    try:
        ##update records if the record already exist in your table
        if result:
            # print ("Full")
            # Update query var need to set as where grp_days='%s', currently it's giving Error
            q2 = "UPDATE crijafData SET Serial_No=%s, date1='%s', date2='%s', Rainfall=%s, TempMaxC=%s, TempMinC=%s, RelHumi_1=%s, RelHumi_2=%s, PanEvapor=%s, BrightSunshine=%s, WindSpeed=%s, SoilTemp_5cm_1=%s, SoilTemp_5cm_2=%s,SoilTemp_15cm_1=%s, SoilTemp_15cm_2=%s, SoilTemp_30cm_1=%s,SoilTemp_30cm_2=%s where grp_days='%s'" % (
                C[length - j][0], x3, x4, C[length - j][2], C[length - j][3], C[length - j][4], C[length - j][5],
                C[length - j][6], checkString, C[length - j][8], C[length - j][9], BL, BL, BL, BL, BL, BL,
                C[length - j][1])
            # q2 = "UPDATE crijafData SET Serial_No=%s, date1=%s, date2=%s, Rainfall=%s, TempMaxC=%s, TempMinC=%s, RelHumi_1=%s, RelHumi_2=%s, PanEvapor=%s, BrightSunshine=%s, WindSpeed=%s, SoilTemp_5cm_1=%s, SoilTemp_5cm_2=%s,SoilTemp_15cm_1=%s, SoilTemp_15cm_2=%s, SoilTemp_30cm_1=%s,SoilTemp_30cm_2=%s where grp_days=%s" % ( C[length-j][0],x3 , x4, C[length-j][2],C[length-j][3],C[length-j][4],C[length-j][5],C[length-j][6],C[length-j][7],C[length-j][8],C[length-j][9],C[length-j][10],C[length-j][11],C[length-j][12],C[length-j][13],C[length-j][14],C[length-j][15], C[length-j][1] )
            print("Update: ", q2)
            x.execute(q2)
        else:

            ##insert records if the new record inserted  in  the organisation website
            # print ("Blank")
            # print(type(C[length -j][7]))

            q3 = "insert into crijafData (Serial_No,date1, date2, grp_days,Rainfall,TempMaxC,TempMinC,RelHumi_1,RelHumi_2,PanEvapor,BrightSunshine,WindSpeed,SoilTemp_5cm_1, SoilTemp_5cm_2,SoilTemp_15cm_1,SoilTemp_15cm_2,SoilTemp_30cm_1,SoilTemp_30cm_2) values (%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                C[length - j][0], x3, x4, C[length - j][1], C[length - j][2], C[length - j][3], C[length - j][4],
                C[length - j][5], C[length - j][6], checkString, C[length - j][8], C[length - j][9], BL, BL, BL, BL, BL,
                BL)
            # q3 = "insert into crijafData (Serial_No,date1, date2, grp_days,Rainfall,TempMaxC,TempMinC,RelHumi_1,RelHumi_2,PanEvapor,BrightSunshine,WindSpeed,SoilTemp_5cm_1, SoilTemp_5cm_2,SoilTemp_15cm_1,SoilTemp_15cm_2,SoilTemp_30cm_1,SoilTemp_30cm_2) values (%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % ( C[length-j][0], x3 , x4, C[length-j][1], C[length-j][2], C[length-j][3], C[length-j][4], C[length -j][5], C[length -j][6], C[length -j][7], C[length -j][8], C[length -j][9], C[length -j][10], C[length -j][11], C[length -j][12], C[length -j][13], C[length -j][14], C[length -j][15] )
            print("INSERT: ", q3)
            x.execute(q3)
            conn.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print("Error: ", e)
        conn.rollback

conn.close()
