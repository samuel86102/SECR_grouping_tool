#import sys
import os
import csv
from datetime import datetime, timedelta

# function of removing the duplicates
def unique(sequence):
    sequence = map(tuple, sequence)
    seen = set()
    data = list([x for x in sequence if not (x in seen or seen.add(x))])
    return [list(x) for x in data] 

def get_id(STR):
    return STR[0:STR.find('-')]

'''
# for testing
input_file='grid2.csv'
output_file='grid2-out.csv'
sdate='2021/05/01'
edate='2021/07/31'
'''
input_file=input('輸入檔案名稱:')
output_file=input('輸出檔案名稱:')
sdate=input('開始日期(ex. 2021/01/01):')
edate=input('結束日期(ex, 2021/07/31):')

print(sdate)
print(edate)

# caculate time span
dt = datetime.strptime(sdate, '%Y/%m/%d')
dt2 = datetime.strptime(edate, '%Y/%m/%d')
d = dt + timedelta(days=1)
delta = dt2 - dt

# create the table for mapping
table=[]
session=1
session_size=3
for i in range(0,delta.days + 1,session_size):
    day = dt + timedelta(days=i)
    for j in range(i,i+session_size):
        table.append([day.strftime('%Y/%m/%d'),session])
        day = day + timedelta(days=1)
    session += 1

# a list to store data
data=[]
with open(input_file, newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        data.append(row)

# some default values
#date_index = 1
#session_index = 3
#id_index = 4
#detector_index = 5
#time_index = 2

# remove duplicates of original data
data = unique(data)

# get the index of attributes
attr=data[0]
for i in range(len(attr)):
    if attr[i]=='Date':
        date_index = i
    if attr[i]=='Session':
        session_index = i
    if attr[i]=='Occasion Detector':
        detector_index = i
    if attr[i]=='Time':
        time_index = i
    if attr[i]=='ID':
        id_index = i

print("============================")
print("Date欄位:", date_index + 1)
print("Session欄位:", session_index+1)
print("Occasion Detector欄位:", detector_index+1)
print("ID欄位:", id_index+1)
print("Time欄位(刪除):", time_index+1)
print("============================")


# add the session
for i in range(1,len(data)):
    date = data[i][date_index]
    for j in range(len(table)):
        if date == table[j][0]:
            data[i][session_index]=table[j][1]
            break


# add final data to data2
data2=[]
data2.append(["Grid","Date","Time","Session","ID","Occasion Detector"])
black_list=[]
for i in range(1, len(data)):
    for j in range(i+1,len(data)):
        if data[i][session_index] == data[j][session_index] and get_id(data[i][detector_index]) == get_id(data[j][detector_index]) and data[i][id_index] == data[j][id_index]:
            black_list.append(data[j])

    date = data[i][date_index]
    dt_date = datetime.strptime(date, '%Y/%m/%d')
    dt_start = datetime.strptime(sdate, '%Y/%m/%d')
    dt_end = datetime.strptime(edate, '%Y/%m/%d')

    if data[i] not in black_list and (dt_date >= dt_start and dt_date <= dt_end):
        data2.append(data[i])





# delete time column
for row in data2:
    del row[time_index]
    del row[date_index]

# output file

with open("tmp.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for e in data2:
        writer.writerow(e)

# reorder columns
with open("tmp.csv", 'r') as infile, open(output_file, 'w') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Grid', 'ID', 'Session', 'Occasion Detector']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

os.remove("tmp.csv")
print("done:D")
