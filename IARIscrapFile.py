from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
import datetime
from datetime import timedelta
import MySQLdb


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


url = 'https://www.iari.res.in/index.php?option=com_content&view=article&id=450&Itemid=224'

page = requests.get(url)
checkNull = page.text
checkCode = page.status_code
# print checkCode
if checkNull != "" and checkCode == 200:
    tree = html.fromstring(page.content)
    # print (tree)
    A = tree.xpath('//table/tbody/tr/td/text()')
    print (A)
    print(len(A))
    B = magicsplit(A, '\r\n', u'\xa00.3*', u'\xa0', u'\xa0', u'\xa0', u'\xa0', u'\xa0', u'\xa0', u'\xa0', u'\xa0',
                   u'\xa0')
    # print (B)
    print(len(B))

    C = [A[i:i + 13] for i in range(24, len(B[0]), 13)]
    #length = len(C[0]) / 13
    print("C: ", C)
    print(len(C))
time = datetime.date.today()
'''conn = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base
x = conn.cursor()

#time2 = "2017-07-25"
#Previous_Date = datetime.datetime.today() - datetime.timedelta(days=50)
time2 = time.strftime('%Y-%m-%d')
##### Check date field full or null
##--------------------------------
result=None
try:
 x.execute("""SELECT * from iari_table where date=%s""", [time2])
 result = x.fetchall()
 print result
 conn.commit()
except:
 conn.rollback

##### Insert today date in database
##---------------------------------
if result:
 print "Full"
else:
 print "Blank"
 try:
  print time2
  #x.execute("""INSERT into iari_table  values (%s)""", [time2])
  x.execute("""INSERT into iari_table  values (%s,'','','','','','','','','','','','')""", [time2])
  conn.commit()
 except Exception,e:
  print str(e)
  #conn.rollback

## Update Record

for i in range(6):
  j=i+1; ## This means in every week before 3 days back log data will update
  print j, ", List: ", C[length-j]
  #t1 =  time - timedelta(days=j)  ## Back one day(-1 as use j+1) from current date
  #current= t1.strftime('%Y-%m-%d')
  #print current, C[length-j][0], C[length-j][2], C[length-j][6], C[length-j][10]
  date2 = datetime.datetime.strptime(C[length-j][0], '%d/%m/%Y')

  try:     
     time3 = date2.strftime('%Y-%m-%d')
     print "Past Time: ", time3
     q2="UPDATE iari_table SET max_temp='"+C[length-j][1]+"', min_temp='"+C[length-j][2]+"', rainfall='"+C[length-j][3]+"', windspeed='"+C[length-j][4]+"', wdc_I='"+C[length-j][5]+"', wdc_II='"+C[length-j][6]+"', weathercon_I='"+C[length-j][7]+"', weathercon_II='"+C[length-j][8]+"', rh_I='"+C[length-j][9]+"', rh_II='"+C[length-j][10]+"', bss='"+C[length-j][11]+"', evap='"+C[length-j][12]+"' where date='"+time2+"' "
     print(q2)
     x.execute(q2)    
     conn.commit()
  except Exception,e:
    print str(e)
    conn.rollback()


conn.close()
'''
