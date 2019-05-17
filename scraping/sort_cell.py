import csv
import sys

sku_scrapped = []
sku_eparts = []
sku_match = []
rows_matching = []


def sort():
    with open('./logic/full_catalog.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            sku = row[1].lower().strip()
            sku_eparts.append(sku)

    with open('./mk_pr_combined.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            for cell in row:
                if 'mfr pn' in cell.lower():
                    try:
                        sku = row[4].split(
                            ':')[1].strip().lower().replace(' ', '')
                    except IndexError:
                        continue
                    for sk in sku.split('/'):
                        if sk in sku_eparts and sku not in sku_match:
                            rows_matching.append(row)

    return rows_matching


def extract():
    headers = []
    rows_matching = sort()
    print(rows_matching)
    with open('./mk_pr_combined.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            for cell in row:
                if ' : ' in cell:
                    if not cell.split(' : ')[0] in headers:
                        headers.append(cell.split(' : ')[0])

    done = []
    with open('./mk_pr_sorted_combined.csv', 'a', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=",")
        writer.writeheader()
        for row in rows_matching:
            obj = {}
            good = True
            # settings keys to unknown
            for key in headers:
                obj[key] = key + " : unknown"

            for cell in row:
                if ' : ' in cell:
                    if 'Mfr PN' in cell.split(' : ')[0]:
                        if cell in done or 'unknown' in cell:
                            good = False
                        else:
                            done.append(cell)

            for cell in row:
                if ' : ' in cell:
                    obj[cell.split(' : ')[0]] = cell.split(' : ')[
                        0] + " : " + cell.split(' : ')[1]

            if good:
                print(obj['Mfr PN'])
                writer.writerow(obj)


if __name__ == "__main__":
    extract()
