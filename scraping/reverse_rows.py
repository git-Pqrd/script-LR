import csv

to_write = []
with open('./csv_to_reverse.csv', 'r') as csv_file: 
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        new_row = []
        new_row_reverse = []
        reversing = False

        for i in row :
            if i == "" : continue
            if "!reverse!" in i   : 
                reversing = True
                continue

            if reversing == False : new_row.append(i)
            else : new_row_reverse.append(i)

        new_row_reverse.reverse()
        new_row += new_row_reverse 
        to_write.append(new_row)

with open('./csv_reversed.csv', 'a')  as csv_file: 
    csv_writer = csv.writer(csv_file, delimiter=',')
    for row in to_write : 
        csv_writer.writerow(row)
