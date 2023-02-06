import sqlite3
import json


class News:
    """
    Модель новостей
    """

    def get_all(self):
        """
        Список новостей
        :return:
        """
        with sqlite3.connect('data\\news.db') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            news = cursor.execute("""
                SELECT 
                    *,
                    (SELECT count(*) FROM comments WHERE news_id = news.id) as 'comments_count'
                FROM news
                WHERE deleted is FALSE AND date < date()
                ORDER BY date DESC""")
            data_list = [dict(idx) for idx in news.fetchall()]
            return data_list

    def get_by_id(self, news_id):
        """
        Получить новость по id
        :param news_id:
        :return:
        """
        with sqlite3.connect('data\\news.db') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    *,
                    (SELECT json_group_array(
                        json_object(
                            'id', id,
                            'news_id', news_id,
                            'title', title,
                            'date', date,
                            'comment', comment
                        )
                     )
                     FROM comments 
                     WHERE news_id = news.id ORDER BY date DESC) as 'comments',
                    (SELECT count(*) FROM comments WHERE news_id = news.id) as 'comments_count'
                FROM news
                WHERE id = ? AND deleted is FALSE AND date < date()""", (int(news_id),))
            news_item = cursor.fetchone()
            if not news_item:
                raise ValueError()
            news_item = dict(news_item)
            news_item['comments'] = json.loads(news_item['comments'])
            return news_item
