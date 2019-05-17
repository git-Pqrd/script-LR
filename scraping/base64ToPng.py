# import glob
import csv
import sys
import base64

csv.field_size_limit(sys.maxsize)
csv_with_base = "./img_iced.csv" #this is the csv with the base64 at the second position
folder_png = "" #folder where to put 

    
    
with open( csv_with_base, 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",") 
    for row in reader :
        sku = row[0].split(' : ')[1]
        img_bs = row[1].split(' : ')[1]
        with open("./../Media/BaseSF/lr_bs_" + sku + ".jpeg", "wb") as fh:
            fh.write(base64.decodebytes(img_bs))
        break


