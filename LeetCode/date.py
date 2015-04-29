#-*-coding:utf8-*-
import random
import string
import csv
from datetime import date,timedelta
def randomaddress():
    storage = 'http://lbsview.service.com/service-lbs/amap-open/locations/adcode/d_adcode::all,d_pkg::com.taobao.taobao/area/'
    yesterday = date.today()-timedelta(days=1)
    time = yesterday.strftime('%Y%m%d')
    end = 25
    datum = ['']
    data = []
    for i in range(0,125):
        hour = i%25
        if end <= hour:
            continue
        if hour == 0:
            end-= 1
        duration = time + str(hour).zfill(2) + '/' + time + str(end)
        datum[0] = duration
        print datum[0]
        data.append(datum[:])
    csvfile = file('date.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(data)
if __name__ == "__main__":
    randomaddress()
        
        
    
