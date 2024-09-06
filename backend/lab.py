import csv
from datetime import datetime 

with open('posts.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    doc = {}
    rubrics = []
    for row in reader:
        text, created_date, rubrics = row
        try:
            print(text[::25], created_date, rubrics[2:-2].split(', '))
        except:
            print('err')