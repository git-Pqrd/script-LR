from bs4 import BeautifulSoup
import requests
import csv



urls = []
with open('Scrapping - epson_scrap.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        urls.append(row[4])


count=0
with open('To_Scrap.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in urls:
        if (i[0] != "h") : continue 
        count +=1
        print(count)
        if (count<5185) : continue
        result = requests.get(i)
        content = result.content
        status = result.status_code
        if status == 200: 
            writer.writerow([i,status,"Y"])
            print(i,status,"Y")
        else : 
            writer.writerow([i,status,"F"])
            print(i,status,"F")

