import csv

cat = "unknown"
headers = []
all_rows = []
counter = {}
important_headers = []

with open('./' + cat + '_iced.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        prod = {}
        for cell in row:
            if cell.split(' : ')[0] not in headers:
                headers.append(cell.split(' : ')[0])
                counter[cell.split(' : ')[0]] = 0
            prod[cell.split(' : ')[0]] = cell

        all_rows.append(prod)


with open('./' + cat + '_sorted_iced.csv', 'a', encoding="utf-8") as csvfile:
    for prod in all_rows:
        for cell in prod:
            counter[cell.split(' : ')[0]] += 1

    for k, v in counter.items():
        if v > 50:
            important_headers.append(k)

    writer = csv.DictWriter(
        csvfile, fieldnames=important_headers, delimiter=";")
    writer.writeheader()

    for prod in all_rows:
        rtw = {}
        for k, v in prod.items():
            if k in important_headers:
                rtw[k] = v
        writer.writerow(rtw)
