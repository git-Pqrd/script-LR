from bs4 import BeautifulSoup
import requests
import csv
import re


result = requests.get('http://www.cetgroupco.com/products/')
content = result.content
status = result.status_code
soup = BeautifulSoup(content, 'html.parser')
urls =  [ 'http://www.cetgroupco.com/products/' + a['href'] for a in soup.find_all('a') ]


count=0
with open('To_Scrap.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in urls:
        if i == 'http://www.cetgroupco.com/products//' : 
            continue

        count +=1
        prod = {}
        images = []
        
        try : 
            result = requests.get(i)
            content = result.content
            status = result.status_code
            soup = BeautifulSoup(content, 'html.parser')

            product_name = soup.find_all('div', class_='pdu-r')[0].find_all('h4')[0].text
            prod['product_name'] = 'product_name : ' + product_name

            for img in  soup.find_all('div', class_='pdu-r')[0].find_all('img') : 
                images.append(img)
            prod['images'] = 'images : ' + product_name

            for row in soup.find_all('table', class_="ptab")[0].find_all('tr') :
                name_carac = row.find_all('td', class_='tleft')[0].get_text(separator="|")
                val_carac = row.find_all('td', class_='tright')[0].get_text(separator="|")
                prod[name_carac] = name_carac + " : " + " ".join([val_carac])

        except : continue

        print(count, prod.values())
        writer.writerow(prod.values())

