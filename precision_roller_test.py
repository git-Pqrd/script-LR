from bs4 import BeautifulSoup
import requests
import csv



urls = []
with open('Scraping - ricoh_to_scrap.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        urls.append(row[2])


count=0
with open('To_Scrap.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in urls:
        if (i == "") : break 
        if (i[0] != "h") : continue 
        count +=1
        result = requests.get(i)
        content = result.content
        status = result.status_code
        soup = BeautifulSoup(content, 'html.parser')
        text_result = soup.find_all('body')[0].find_all('h1')[0].text

        if text_result != 'Search Our Catalog' : 
            writer.writerow([i,text_result,"Y"])
            print(count, i,text_result,"Y")
        else : 
            writer.writerow([i,text_result,"F"])
            print(count, i,text_result,"F")

