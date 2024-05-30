"""Загрузчик данных в SQLite."""
import csv
import logging

from api_yamdb.reviews.models import Category

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


def load_to_sql(dataReader):
    line = 0
    for line in dataReader:
        if line != 0:
            category = Category.objects.create()
            category.id = line[0]
            category.review = line[1]
            category.text = line[2]
            category.author = line[3]
            category.pub_date = line[4]
            category.save()
        else:
            line += 1


for file_name in csv_files_names:
    dataReader = csv.reader(open(file_name), delimiter=',')
    load_to_sql(dataReader)
