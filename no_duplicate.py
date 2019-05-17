import csv


new_csv = []
seen_ean = []
count_all = 0
count_good = 0

with open('./scraping/wip_ConsoToGet.csv', 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        count_all += 1
        print(row)
        if row[2] in seen_ean:
            continue
        else:
            count_good += 1
            seen_ean.append(row[2])
            new_csv.append(row)


with open('./scraping/consotoget_no_dup.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for i in new_csv:
        writer.writerow(i)

print(str(count_all) + ' - ' + str(count_good))
