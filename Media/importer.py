from fake_useragent import UserAgent
import requests
import csv
import sys
import os
import argparse
import time

parser = argparse.ArgumentParser()
# getting the mandatory output file
parser.add_argument('-f', type=str, help='le fichier qui contient les urls')
parser.add_argument('-o', type=str, help='le folder output ou tu mets les medias')
parser.add_argument('-m', type=str, help='nom du fichier avec les sku et les noms des images')
args = parser.parse_args()

if args.f is not None :
    print('fichier inclus ' + args.f)
    if 'csv' in args.f : 
        file_name = args.f
    else :
        file_name = args.f + ".csv"
else : 
    print('pas de fichier inclus')
    sys.exit


if args.o is not None :
    print('folder output inclus ' + args.o)
    upload_folder = args.o
else : 
    print('pas de fichier output je pars sur out_' + file_name[:4] )
    upload_folder = file_name[:4]

if args.m is not None :
    print('fichier csv recapitulatif inclus --> ' + args.m)
    if 'csv' in args.m : 
        done_file_name = args.m
    else :
        done_file_name = args.m + ".csv"
else : 
    print('pas de fichier csv recapitulatif inclus je pars sur out_' + file_name )
    done_file_name = 'out_' + file_name


ua = UserAgent()
sku_img_done = []  # not reimporting done
new_row = []

try : 
    with open(done_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            sku_img_done.append(row[0])
except FileNotFoundError : 
    print("fichier n'existe pas je le crée")


with open(file_name, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for row in reader:
        sku = row[1]
        img = row[2]

        if sku in sku_img_done:
            print("done")
            continue

        if 'http' not in img:
            continue

        prefix = 'lr_'
        suf = '_'
        fix = 0
        extension = img.split('.')[-1]
        suffix = suf + str(fix)
        nom_img = prefix + str(sku) + suffix

        while nom_img + '.' + extension in (row[2] for row in new_row):
            fix += 1
            suffix = suf + str(fix)
            nom_img = prefix + str(sku) + suffix

        nom_img = nom_img+'.'+extension
        headers = {'User Agent': ua.random}
        r = requests.get(img, allow_redirects=True, headers=headers)

        try:
            with open( upload_folder +'/'+ nom_img, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        except FileNotFoundError : 
            os.mkdir('./'+upload_folder)
            with open( upload_folder +'/'+ nom_img, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        except requests.exceptions.SSLError:
            time.sleep(5)

        new_row.append([sku, img, nom_img])
        print('downloading - ' + nom_img)

        with open(done_file_name, 'a') as done_csvfile:
            writer = csv.writer(done_csvfile, delimiter=',')
            writer.writerow([sku, img, nom_img])
