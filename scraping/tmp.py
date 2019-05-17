import csv

with open('./unknown_sorted_iced.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for row in reader :
        if 'C13T12854511' in row[29] :
            print(row)
