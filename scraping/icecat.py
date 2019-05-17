from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
# StaleElementReferenceException,
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
opts = FirefoxOptions()
# opts.add_argument("--headless") #export DISPLAY=:0.0

eans = []
cat = "unknown"
count = 0
count_all = 0
try:
    with open('./' + cat + '_iced.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            for cell in row:
                if 'ean : ' in cell:
                    ean = cell.split(' : ')[1].strip()
                    eans.append(ean)
except FileNotFoundError:
    pass


driver = webdriver.Firefox(firefox_options=opts)


def go_and_get(ean):
    url = "http://prf.icecat.biz/?shopname=StephanPire&ean_upc=" + ean + "&lang=en"
    # url = "http://prf.icecat.biz/api/?UserName=openIcecat-live&Language=en&ean_upc=" + ean
    driver.get(url)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.IcecatLive")))
    except:
        return

    print(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    prod = {}

    prod["ean"] = "ean : " + ean

    prod["full_name"] = "full_name : " + driver.find_element(
        By.XPATH, '//*[@id="loadLiveIcecat"]/div/div/div/div/div[1]/div/span').text
    prod["short_name"] = "short_name : " + driver.find_element(
        By.XPATH, '//*[@id="loadLiveIcecat"]/div/div/div/div/div[2]/div[2]/div/div/div[2]/span[2]').text
    prod["brand"] = "brand : " + driver.find_element(
        By.XPATH, '//*[@id="loadLiveIcecat"]/div/div/div/div/div[2]/div[2]/div/div/div[1]/span[2]').text
    prod["sku"] = "sku : " + driver.find_element(
        By.XPATH, '//*[@id="loadLiveIcecat"]/div/div/div/div/div[2]/div[2]/div/div/div[3]/span[2]').text

    try:
        img = "img : " + \
            soup.find('div', id='liveMainImage').find_all('img')[0]['src']
    except AttributeError:
        img = "img : noImg"

    for kv in soup.find_all('div', class_='-icecat-tableRow'):
        key = kv.find_all(
            'div', class_='-icecat-ds_label')[0].text.strip().replace("\n", "").replace('"', '').replace('\r', '')
        val = kv.find_all(
            'div', class_='-icecat-ds_data')[0].text.strip().replace("\n", "").replace('"', '').replace('\r', '')
        prod[key] = key + " : " + val

    with open('./' + cat + '_iced.csv', 'a', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(prod.values())

    if "noImg" not in img:
        with open('./img_iced.csv', 'a', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow([prod["sku"], img])

    print(prod.values())


with open('./' + cat + '_to_ice.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for x in reader:
        count_all += 1

with open('./' + cat + '_to_ice.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        ean = row[7]
        brand = row[0]
        sku = row[1]
        count += 1
        if any(l.isalpha() for l in ean):
            print(ean + " has alpha")
            continue
        if ean in eans:
            print(ean + " has been done")
            continue
        go_and_get(ean)

driver.close()
