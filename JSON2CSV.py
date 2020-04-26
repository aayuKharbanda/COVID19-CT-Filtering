import json
import datetime
import csv
id =1
#id of the person being analysed can be iterated when we have sufficient data

#input users latest month data in a json file , here test_monthly.json
with open('test_monthly.json') as json_file :
    data = json.load(json_file)
#     print(data)
    count = 0
    final = []
    temp = ['ID','EntryNo','Latitude','Longitude','StartTime','EndTime','Confidence']
    final.append(temp)
    for pv in data['timelineObjects'] :
        latitude = 0
        longitude = 0
        confidence = 0
        start = 0
        end = 0
        
        for x in pv.values() :
            all_keys = list( x.keys())
            if(all_keys[0]!='location'):
                continue
#             print(all_keys)
            count = count +1
    
            latitude = x['location']['latitudeE7']
            longitude = x['location']['longitudeE7']
            confidence = x['location']['locationConfidence']
            start = x['duration']['startTimestampMs']
            end = x['duration']['endTimestampMs']
            confidence = int(confidence)
            start = int(start)
            start = datetime.datetime.fromtimestamp(start / 1e3)
            end = int(end)
            end = datetime.datetime.fromtimestamp(end / 1e3)
            
            entry = []
            entry.append(id)
            entry.append(count)
            entry.append(latitude)
            entry.append(longitude)
            entry.append(str(start))
            entry.append(str(end))
            entry.append(confidence)
            
#             print('For entry number' + str(count))
#             print('latitude is ' + str(latitude))
#             print('longitude is ' + str(longitude))
#             print('confidence is ' + str(confidence))
#             print('we get time in IST')
#             print('start moment is ' + str(start))
#             print('end moment is ' + str(end))
#             print(entry)
#             print(entry)
        
            final.append(entry)
           

    # print(final)
    


#the list of list final is converted into a csv file as temp_out.csv
with open("temp_out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final)
