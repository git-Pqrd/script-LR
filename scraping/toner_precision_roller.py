from bs4 import BeautifulSoup
import requests
import csv
import re
import os  


#
def parse(brand) :
    file_name = './precision_roller/toner_cartridge_'+ brand + '.csv'
    result = requests.get('https://www.precisionroller.com/category/toner-cartridges/'+brand+'.htm')
    content = result.content
    status = result.status_code
    soup = BeautifulSoup(content, 'html.parser')
    urls =  [ a["href"] for a in soup.find_all('a', class_='model_link')]

    #I expect ot be evinced anytime so playing it safe with the csv a row visited is written
    rows_written = []
    if os.path.isfile('./'+ file_name ): #this is is to avoid any error if i deleted the mf
        with open(file_name ,'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader :
                rows_written.append(row[0])

    count=0
    with open( file_name , 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for i in urls:
            count +=1
            if i in rows_written : 
                print(str(count) + " done")
                continue
            prod = {}

            #getting the content
            result = requests.get(i)
            content = result.content
            status = result.status_code
            soup = BeautifulSoup(content, 'html.parser')

            
            #getting multiple li to class the one conso and the one spare
            box_model = soup.find_all('h1')[0].parent.findChildren("table" , recursive=False)
            if len(box_model) > 0 : 
                for box in box_model : 
                    link    = box.find_all('a', class_='title_link')[0]
                    title   = box.find_all('tr')[0].find_all('td')[0].text.replace('\r', '').replace('\n', '').replace('\t', '')
                    if "Cost-Saving" not in title.split(" "): 
                        result = requests.get(link['href'])
                        content = result.content
                        status = result.status_code
                        soup = BeautifulSoup(content, 'html.parser')
                        continue

            if "Cost-Saving" in title.split(" ") : continue

            prod["product_name"]  = "product_name : " + soup.find_all('h1')[0].text.replace('\n', '').replace('\t', '').replace('\r', '')
            try : prod["img"]  = "img : https://www.precisionroller.com" + soup.find_all('a', class_="fancyimg")[0]["href"]
            except : prod["img"] = "img : placeholder"


            try : prod_info = soup.find('div', id='product_resources').find_all('table' , class_='grey')[0]
            except : continue
            for li in prod_info.find_all('li') : 
                key_prod = ' '.join(li.text.strip().replace('\t',' ').replace('\n','').replace('  ',' ').split('\r')).split(':')[0]
                val_prod = ' '.join(li.text.strip().replace('\t',' ').replace('\n','').replace('  ',' ').split('\r')).split(':')[1].strip()
                prod[key_prod] = key_prod + ' : ' + val_prod

            try : 
                prod_model = soup.find('div', id='product_resources').find_all('table' , class_='grey')[1]
                prod_model_all = [a.text for a in prod_model.find_all('a')]
                prod["model_compat"] = "model_compat : " + '|'.join(prod_model_all)
            except : 
                prod_model = "model_compat : NULL" 

            print(prod["product_name"])
            writer.writerow([i] + list(prod.values()))

brands = [ "brother", "dell", "epson", "hp", "kyocera", "lexmark", "okidata", "panasonic", "ricoh", "samsung",
        "sharp","toshiba","xerox"]

for brand in brands :
    parse(brand)
