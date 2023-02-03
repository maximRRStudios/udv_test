import json
import sqlite3

NEWS_FILE = 'news.json'

COMMENTS_FILE = 'comments.json'


def init_db():
    """
    Инициализация БД Sqllite
    :return:
    """
    with sqlite3.connect('data\\news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS news')
        cursor.execute('DROP TABLE IF EXISTS comments')
        cursor.execute('CREATE TABLE news (id PRIMARY KEY, title text, date text, body text, deleted integer)')
        cursor.execute('CREATE TABLE comments (id PRIMARY KEY, news_id integer, title text, date text, comment text)')
        cursor.execute('CREATE INDEX news_filter ON comments (news_id)')


def load_data():
    """
    Заполнение БД
    :return:
    """
    with sqlite3.connect('data\\news.db') as connection:
        cursor = connection.cursor()
        with open(NEWS_FILE, encoding='utf-16') as news_src:
            news_json = json.loads(news_src.read())
            cursor.executemany('INSERT INTO news values (:id, :title, :date, :body, :deleted)', news_json['news'])

        with open(COMMENTS_FILE, encoding='utf-16') as comments_src:
            comments_json = json.loads(comments_src.read())
            cursor.executemany('INSERT INTO comments values (:id, :news_id, :title, :date, :comment)', comments_json['comments'])
