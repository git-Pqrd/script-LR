import glob
import os
import csv

count = 0
row_to_write = []

for x, file in enumerate(glob.glob("./precision_roller/mai*.csv")):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            row_to_write.append(row)


with open('./mk_pr_combined.csv', mode='a') as combine:
    combine_writer = csv.writer(
        combine, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in row_to_write:
        combine_writer.writerow(row)
