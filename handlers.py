from aiohttp import web
import sqlite3
import json


class Handlers:
    """
    Класс обработчиков реквестов
    """

    @staticmethod
    async def news(request):
        """
        Обработчик для Get "/"
        :param request:
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
            result_json = json.dumps({'news': data_list, 'news_count': len(data_list)}, indent=4)
            return web.Response(text=result_json, content_type='application/json')

    @staticmethod
    async def get_news_by_id(request):
        """
        Обработчик для запроса новости по id
        :param request:
        :return:
        """
        news_id = request.match_info['id']
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
                raise web.HTTPNotFound()
            news_item = dict(news_item)
            news_item['comments'] = json.loads(news_item['comments'])
            result_json = json.dumps(dict(news_item), indent=4)
            return web.Response(text=result_json, content_type='application/json')
