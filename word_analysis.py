import csv
words= []
with open('spare.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
         csv_words = row[0].split(" ")
         for i in csv_words:
              words.append(i)

words_counted = []
for i in words:
    x = words.count(i)
    words_counted.append((i,x))

#write this to csv file
word_printed = []
for word in words_counted :
    if word[1] > 1000 and word not in word_printed :
        word_printed.append(word)
        print (word)
