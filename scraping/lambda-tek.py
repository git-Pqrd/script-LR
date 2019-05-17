from bs4 import BeautifulSoup
import requests
import csv
import re
import os


sku_i_need = []
with open('./skus_lambda.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        sku_i_need.append(row[0])

file_name = './lambdatek/'
new_row = []

for i in range(1, 4):
    result = requests.get(
        'https://www.lambda-tek.com/shop/?region=GB&catid=0&searchString=Maintenance%20Kit&show=&itemsperpage=400&page=' + str(i))
    content = result.content
    status = result.status_code
    soup = BeautifulSoup(content, 'html.parser')

    for elem in soup.find_all(class_='valignl'):
        sku = elem.get_text().split('Mfr Num: ')[1].split('\n')[0]
        if sku in sku_i_need:
            prod = {}
            result = requests.get(elem.find_all(
                'a')[0]['href']+'&viewSpec=y#product-view')
            content = result.content
            status = result.status_code
            soup = BeautifulSoup(content, 'html.parser')
            try:
                prod['long_name'] = soup.find_all('h4', class_='prodsubtitle')[
                    0].get_text().strip()
            except:
                continue

            try:
                prod['img'] = 'img : ' + \
                    soup.find_all(
                        'img', class_='img-responsive product-imagePr')[0]['src']
            except:
                img = "img : unknown"

            try:
                for pdt in soup.find_all('ul', class_='prodDetails')[0].find_all('li'):
                    key = pdt.get_text().split(':')[0].strip()
                    val = pdt.get_text().split(':')[1].strip()
                    prod[key] = val
            except:
                pass

            try:
                for table in soup.find_all('table', class_='table-striped'):
                    for tr in table.find_all('tr'):
                        if len(tr.find_all('td')) == 2:
                            key = tr.find_all('td')[0].get_text().strip()
                            val = tr.find_all('td')[1].get_text().strip()
                            prod[key] = val
            except:
                pass

            new_row.append(prod)
            break

for row in new_row:
    print(row)
    print(row.keys())
    print(row.values())

# with open('./lambda-mk.csv', 'a') as csvfile:
    # writer = csv.DictWriter(csvfile, delimiter=",")
    # writer.writerow(prod)
    # pass
