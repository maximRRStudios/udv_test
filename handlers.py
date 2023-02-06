from aiohttp import web
import sqlite3
import json
from news import News


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
        model = News()
        news_list = model.get_all()
        result_json = json.dumps({'news': news_list, 'news_count': len(news_list)}, indent=4)
        return web.Response(text=result_json, content_type='application/json')

    @staticmethod
    async def get_news_by_id(request):
        """
        Обработчик для запроса новости по id
        :param request:
        :return:
        """
        news_id = request.match_info['id']
        model = News()
        try:
            item = model.get_by_id(news_id)
            result_json = json.dumps(dict(item), indent=4)
            return web.Response(text=result_json, content_type='application/json')
        except ValueError:
            raise web.HTTPNotFound()
