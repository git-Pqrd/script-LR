from bs4 import BeautifulSoup
import requests
import csv
import re
import os


file_name = './cartridge_save/label_paper.csv'
result = requests.get(
    'https://www.cartridgesave.co.uk/label-tape/Brother.html')
content = result.content
status = result.status_code
soup = BeautifulSoup(content, 'html.parser')
boxes = soup.find_all('ul', class_="printer_list")
urls = []
for box in boxes:
    urls += [a["href"] for a in box.find_all('a')]

count = 0
# I expect ot be evinced anytime so playing it safe with the csv a row visited is written
rows_written = []
if os.path.isfile('./' + file_name):  # this is is to avoid any error if i deleted the mf
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            rows_written.append(row[0])

with open(file_name, 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in urls:
        count += 1
        prod = {}

        # getting the content
        result = requests.get(i)
        content = result.content
        status = result.status_code
        soup = BeautifulSoup(content, 'html.parser')

        # getting multiple li to class the one conso and the one spare
        for section in soup.find_all('div', class_='section-item-info'):
            for li in section.find_all("li", class_='product-item'):
                for a in li.find_all("a", class_='product-item-link'):
                    if "Genuine" in a.text and a["href"] not in rows_written:
                        type_raw = section.find_all(
                            'div', class_='group-name')[0]
                        type_conso_full = "type_conso : " + type_raw.text
                        type_conso = "type_conso : " + \
                            type_raw.find_all('strong')[0].text
                        url = "url : " + a["href"]
                        # they lazy load so taking the data-src one
                        img = "img : " + \
                            li.find_all(
                                'a', class_="product-item-photo")[0]['data-image-src']
                        name = "name : " + a.get_text()
                        rows_written.append(a["href"])
                        writer.writerow([url, type_conso,  img, name])
                        print([type_conso, type_conso_full, url, img, name])
                        print(count)
