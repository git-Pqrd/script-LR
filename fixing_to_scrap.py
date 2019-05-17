import csv
import re

count=0
new_array = []
with open('To_Scrap.csv', 'r') as csvfile:
    reader = csv.reader(
            [x.replace('\n', '').replace('\r', '').replace('\0', '') for x in csvfile], delimiter=",")
    for row in reader:
        if ("Grade" not in row[0]): 
            new_array.append(["P"]+row)
        else : 
            new_array.append(["G"]+row)

with open('To_fixed_Scrap.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for r in new_array :
        writer.writerow(r)




