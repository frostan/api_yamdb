"""Загрузчик данных в SQLite."""
import logging
from api_yamdb.reviews.models import *

import csv


_log_format = '%(asctime)s, [%(levelname)s], %(message)s, %(funcName)s'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(_log_format))
logger.addHandler(handler)

csv_files_names = [
    'category.csv',
    'comments.csv',
    'genre.csv',
    'genre_title.csv',
    'review.csv',
    'titles.csv',
    'users.csv'
]

def load_to_sql (dataReader):
    line = 0
    for line in dataReader:
        if line <> 0:
            category=Category()
            category.id=row[0]
            category.review=row[1]
            category.text=row[2]
            category.author=row[3]
            category.pub_date=row[4]
            category.save()
        else line += 1

for file_name in csv_files_names:
    dataReader = csv.reader(open(file_name), delimiter=',')
    load_to_sql (dataReader)



