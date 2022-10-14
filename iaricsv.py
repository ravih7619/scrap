import csv
import MySQLdb
import datetime
from datetime import timedelta

time=datetime.date.today()
sysDate = datetime.datetime.now()
print sysDate, time
compareDate = datetime.datetime.strptime (str(time),'%Y-%m-%d').strftime('%d-%m-%Y')
print "CompareDate: ",compareDate

db = MySQLdb.connect(host="10.100.3.74",    # your host, usually localhost
                     user="krishi_observ",         # your username
                     passwd="Observ@41",  # your password
                     db="krishi_observ")        # name of the data base
cursor = db.cursor()

csv_data = csv.reader(file('iari_table.csv'))
for row in csv_data:

     result=None
     try:
	  ##update records if the record already exist in your table
          if (result):  
             cursor.execute("UPDATE iari_table SET max_temp='%s', min_temp='%s', rainfall='%s', windspeed='%s', wdc_I='%s', wdc_II='%s', weathercon_I='%s', weathercon_II='%s', rh_I='%s', rh_II='%s', bss='%s', evap='%s' where date='%s'" % (max_temp, min_temp, rainfall, windspeed, wdc_I, wdc_II, weathercon_I, weathercon_II, rh_I, rh_II, bss, evap,date) )
         
           
          else: 
            cursor.execute('INSERT INTO iari_table(date, max_temp, min_temp, rainfall, windspeed, wdc_I, wdc_II, weathercon_I, weathercon_II, rh_I, rh_II, bss, evap)''VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', row)
         
       
          db.commit()      
     except Exception ,e:
           print str(e)

    #cursor.execute('INSERT INTO iari_table(date, max_temp, min_temp, rainfall, windspeed, wdc_I, wdc_II, weathercon_I, weathercon_II, rh_I, rh_II, bss, evap)''VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s")', row)
           print row

           db.close()
#print "Done"


