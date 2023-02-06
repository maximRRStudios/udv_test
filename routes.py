from aiohttp import web
from handlers import Handlers


def setup_routes(app: web.Application):
    """
    Настройки роутинга
    :param app:
    :return:
    """
    app.router.add_get('/', Handlers.news)
    app.router.add_get(r'/news/{id:\d+}', Handlers.get_news_by_id)
