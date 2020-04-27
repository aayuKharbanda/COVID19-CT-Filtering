import pandas as pd
import datetime
output = []
g_df = pd.read_csv("temp_out.csv")
s_df = pd.read_csv("temp_out2.csv")
print(g_df)
print(s_df)
g_rows = g_df.shape[0]
s_rows = s_df.shape[0]

for x in range(g_rows):
    g_lat = g_df.at[x,'Latitude']
    g_long = g_df.at[x,'Longitude']
    g_start = g_df.at[x,'StartTime']
    g_end = g_df.at[x,'EndTime']
    g_confidence = g_df.at[x,'Confidence']
    for y in range(s_rows):
        
        s_lat = s_df.at[y,'Latitude']
        s_long = s_df.at[y,'Longitude']
        s_start = s_df.at[y,'StartTime']
        s_end = s_df.at[y,'EndTime']
        s_confidence = s_df.at[y,'Confidence']
#         print(g_lat,s_lat)
        if((s_lat == g_lat) and (s_long == g_long) and (s_end >= g_start) and (g_end >= s_start)):
            
            temp = []
            temp.append(s_lat)
            temp.append(s_long)
            s = max(s_start,g_start)
            s = datetime.datetime.fromtimestamp(s / 1e3)
            e = min(s_end,g_end)
            e = datetime.datetime.fromtimestamp(e / 1e3)
            temp.append(str(s))
            temp.append(str(e))
            temp.append((s_confidence * g_confidence*1.0)/100)
            output.append(temp)
    
print(output)    

swa_long = s_df['Longitude'].tolist()
swa_lati = s_df['Latitude'].tolist()
guddu_long = g_df['Longitude'].tolist()
guddu_lati = g_df['Latitude'].tolist()

from matplotlib import pyplot as plt
plt.plot( swa_lati, swa_long)
plt.plot(guddu_lati,guddu_long)
intersect = []
for i in range(len(swa_long)):
    for j in range(len(guddu_long)):
        if((swa_long[i] == guddu_long[j]) and (swa_lati[i] == guddu_lati[j])):
            temp = []
            temp.append(swa_lati[i])
            temp.append(swa_long[i])
            
            intersect.append(temp)
        
            
for x in intersect:
    print(x) 
plt.show()
