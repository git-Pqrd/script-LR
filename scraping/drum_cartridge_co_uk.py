from bs4 import BeautifulSoup
import requests
import csv
import re
import os  



file_name = './cartridge_save/drum_cartridge_save_co_uk.csv'

count=0
#I expect ot be evinced anytime so playing it safe with the csv a row visited is written
urls_visited = []

if os.path.isfile('./'+ file_name ): #this is is to avoid any error if i deleted the mf
    with open(file_name ,'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader :
            urls_visited.append(row[0])

with open( file_name , 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in range(55): 
        result = requests.get('https://www.cartridgesave.co.uk/search/?p='+str(i)+'&q=drum')
        content = result.content
        status = result.status_code
        soup = BeautifulSoup(content, 'html.parser')
        urls = []
        urls += [ a["href"] for a in soup.find_all('a', class_='product-item-link') ]

        for i in urls:
            count += 1
            #getting the content
            result = requests.get(i)
            content = result.content
            status = result.status_code
            soup = BeautifulSoup(content, 'html.parser')

            #getting multiple li to class the one conso and the one spare
            try : name = "product_name : " + soup.find_all('h1', class_='page-title')[0].text
            except : 
                print("ressource not found : "+ i)
                continue

            try : img = soup.find_all('meta', {'itemprop': 'image'})[0]['content']
            except : img = "Unknown"

            try : nmbr_page = "nmbr_page : " + soup.find_all('span', class_='yield')[0].text
            except : nmbr_page = "unknown" 

            color = "color : " + "|".join(soup.find_all('span', class_='sprite')[0]['class'])
            # except : color = "incolor" 
            # try : 
            desc = "desc : " + soup.find_all('div', class_='inner-content article')[0].find_all('p')[0].get_text(separator=". ")

            compat_printer = "model_compatible : "
            try : 
                for a in soup.find_all('div', class_="compatible_printers")[0].find_all('a', class_='p_link'): 
                    compat_printer = compat_printer + a.text+"|"
            except : 
                compat_printer = "unknown"

            product_spec =  []
            for tr in soup.find_all('table', class_='additional-attributes')[0].find_all('tr'):
                carac_key = tr.find_all('th')[0].get_text(separator=". ")
                carac_val = tr.find_all('td')[0].get_text(separator=". ")
                product_spec.append(carac_key + " : " + carac_val )

            urls_visited.append(i)
            row_done = [i, name ,  img , nmbr_page, color, desc] + [compat_printer] + product_spec 
            writer.writerow(row_done)
            print(row_done)

