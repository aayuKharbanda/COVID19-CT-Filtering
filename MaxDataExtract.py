#put input file name into jasonName assuming it is in same directory as the code
import time
start_time = time.time()


jasonName = 'test_monthly2.json'
outName= jasonName.split('.')
outName = outName[0]
id = outName
outName = outName + '_out.csv'
print(outName)
splitSize = 60000
#if you want intervals of size one minute put split = 1
split = 1
#if you want standard datetime format for time put ts = 0
ts = 0

import json
import datetime

import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit as pfit

#id of the person being analysed can be iterated when we have sufficient data



##------------------- note---------------------------##
## convert late7 to latitudee7 and same for lnge7

def findLen(x,y):
    temp = x**2 + y**2
    return temp**(0.5)

def entrymaker(latitude,longitude,id,count,start,end,confidence):

    if(ts==0):
        start = datetime.datetime.fromtimestamp(start / 1e3)
        end = datetime.datetime.fromtimestamp(end / 1e3)
        
    latitude = (latitude*1.0)/10000000
    longitude = (longitude*1.0)/10000000
    entry = []
    entry.append(id)
    entry.append(count)
    if(confidence == -1):
        entry.append('active')
    else:
        entry.append('static')
    
    entry.append(latitude)
    entry.append(longitude)
    entry.append(str(start))
    entry.append(str(end))
    
    entry.append(confidence)
    
    
    return entry
   

def dynamic(x,final,count):
    start = int(x['duration']['startTimestampMs'])
    end = int(x['duration']['endTimestampMs'])
    confidence = -1
    seg = 1
    dynamiclat = []
    dynamiclong = []
    if ('latitudeE7' in (x['startLocation']).keys()):
        dynamiclat.append(x['startLocation']['latitudeE7'])
        dynamiclat.append(x['endLocation']['latitudeE7'])
        dynamiclong.append(x['startLocation']['longitudeE7'])
        dynamiclong.append(x['endLocation']['longitudeE7'])
    else:
        dynamiclat.append(x['startLocation']['latE7'])
        dynamiclat.append(x['endLocation']['latE7']) 
        dynamiclong.append(x['startLocation']['lngE7'])
        dynamiclong.append(x['endLocation']['lngE7'])
         
    
 
    if('waypointPath' in x.keys()):
        for y in x['waypointPath']['waypoints']:
            if('latitudeE7' in y.keys()):
                dynamiclat.append(y['latitudeE7'])
                dynamiclong.append(y['longitudeE7'])
            else:
                dynamiclat.append(y['latE7'])
                dynamiclong.append(y['lngE7'])
            
    if('simplifiedRawPath' in x.keys()):
        for y in x['simplifiedRawPath']['points']:
            if('latitudeE7' in y.keys()):
                dynamiclat.append(y['latitudeE7'])
                dynamiclong.append(y['longitudeE7'])
            else:
                dynamiclat.append(y['latE7'])
                dynamiclong.append(y['lngE7'])
    

    distance = 0
    for i in range(len(dynamiclat)-1):
        lat1 = dynamiclat[i]
        lat2 = dynamiclat[i+1]
        long1 = dynamiclong[i]
        long2 = dynamiclong[i+1]
        t1 = lat1 - lat2
        t2 = long1 - long2
        temp = t1**2 + t2**2
        distance += temp**(0.5)
        
    time = (end - start)
    speed = distance/time
    totalseg = int(time/6000)
#     print(distance, time ,speed )
    new_long = []
    new_lat = []
    new_time = []
    newstart = start
    for i in range(0,len(dynamiclat)-1):
        dx = 0
        dy = 0
        lat1 = dynamiclat[i]
        lat2 = dynamiclat[i+1]
        long1 = dynamiclong[i]
        long2 = dynamiclong[i+1]
        temp = (lat1 - lat2)**2 + (long1 - long2)**2
        temp = temp**(0.5)
        seg = totalseg * (temp/distance)
        seg = int(seg)
        print(seg)
        seg = max(1,seg)
        dx = lat1 - lat2
        dy = long1 - long2
        dx = dx /seg
        dy = dy/seg
        for j in range(seg):
            new_lat.append(lat1 - dx*j)
            new_long.append(long1 - dy*j)
            new_time.append(newstart + (findLen(dx*j,dy*j))/speed) 
            newstart +=  (findLen(dx*j,dy*j))/speed
            
    for i in range(len(new_lat)):
        final.append(entrymaker(new_lat[i],new_long[i],id,count,new_time[i],new_time[i] + 6000,confidence))
        count = count +1
        
    final.append(entrymaker(dynamiclat[-1],dynamiclong[-1],id,count,new_time[-1],new_time[-1] + 6000,confidence))
    count = count +1
    
    plt.plot(dynamiclat,dynamiclong, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12) 
    plt.show()
   
#     print(speed)
    
    if(speed < 0.20):
        text = 'slow'
    if(speed <= 1.00 and speed >= 0.2):
        text = 'medium' 
    if(speed > 1.0):
        text = 'high'
    print('speed of activity is '+ text)
    plt.plot(new_lat,new_long, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12) 
    
    
    plt.show()
    plt.clf()
    
    return count

with open(jasonName) as json_file :
    data = json.load(json_file)
#     print(data)
    count = 0
    final = []
    temp = ['ID','EntryNo','Data Type','Latitude','Longitude','StartTime','EndTime','Confidence']
    final.append(temp)
    for pv in data['timelineObjects'] :
        latitude = 0
        longitude = 0
        confidence = 0
        start = 0
        end = 0
        
        for x in pv.values() :
            all_keys = list( x.keys())
#             print(all_keys)
            if((all_keys[0]=='startLocation') ):
                print('activity record')
                count = dynamic(x,final,count)
                continue

            if((all_keys[0] =='location') ):
#                 print('normal location')
                if('latitudeE7' in x['location'] ):
                    latitude = x['location']['latitudeE7']
                    longitude = x['location']['longitudeE7']
                    confidence = x['location']['locationConfidence']
                    start = int(x['duration']['startTimestampMs'])
                    end = int(x['duration']['endTimestampMs'])
                if('latE7' in x['location'] )  :
                    latitude = x['location']['latE7']
                    longitude = x['location']['lngE7']
                    confidence = x['location']['locationConfidence']
                    start = int(x['duration']['startTimestampMs'])
                    end = int(x['duration']['endTimestampMs'])
                    
                    if(split ==1 ):
                        while(start+splitSize < end):
                            final.append(entrymaker(latitude,longitude,id,count,start,start+splitSize,confidence))
                            start = start + splitSize
                            count = count +1
                        final.append(entrymaker(latitude,longitude,id,count,start,start+splitSize,confidence))
                        count = count +1
                    else:
                        final.append(entrymaker(latitude,longitude,id,count,start,end,confidence))
                        count = count +1
                else:
                    start = int(x['duration']['startTimestampMs'])
                    end = int(x['duration']['endTimestampMs'])

              
                
            if 'otherCandidateLocations' in x.keys() :
                for y in x['otherCandidateLocations']:
#                     print('abnormal locations')
                    if('latitudeE7' in y.keys()):
                        latitude = y['latitudeE7']
                        longitude = y['longitudeE7']
                        confidence = y['locationConfidence']
                    else:
                        latitude = y['latE7']
                        longitude = y['lngE7']
                        confidence = y['locationConfidence']
                   
                               
                    if(split ==1):
                        while(start+splitSize < end):
                            final.append(entrymaker(latitude,longitude,id,count,start,start+splitSize,confidence))
                            count = count +1
                            start = start + splitSize
                        final.append(entrymaker(latitude,longitude,id,count,start,start+splitSize,confidence))
                        count = count +1
                    else:
                        final.append(entrymaker(latitude,longitude,id,count,start,end,confidence))
                        count = count +1
                    

            
#     print(final)

import csv
#the list of lists final is converted into a csv file as temp_out.csv
with open(outName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final)

print("--- %s seconds ---" % (time.time() - start_time))