import glob
import csv

all_files = glob.glob('./img/*')

new_row = []
new_row.append(['sku', 'base_image'])

for a_file in all_files:
    sku = a_file.split('_')[1]
    base_image = a_file.split('/')[-1]
    new_row.append([sku, base_image])

with open('./import_img.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    for row in new_row:
        writer.writerow(row)
