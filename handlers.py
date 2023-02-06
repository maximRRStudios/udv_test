from aiohttp import web
from news import News


class Handlers:
    """
    Класс обработчиков реквестов
    """

    @staticmethod
    async def news(request: web.Request) -> web.Response:
        """
        Обработчик для Get "/"
        :param request:
        :return:
        """
        model = News()
        news_list = model.get_all()
        return web.json_response({'news': news_list, 'news_count': len(news_list)})

    @staticmethod
    async def get_news_by_id(request: web.Request) -> web.Response:
        """
        Обработчик для запроса новости по id
        :param request:
        :return:
        """
        news_id = request.match_info['id']
        model = News()
        try:
            item = model.get_by_id(int(news_id))
            return web.json_response(item)
        except ValueError:
            raise web.HTTPNotFound()
