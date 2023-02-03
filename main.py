from aiohttp import web
from data_loader import init_db, load_data
from routes import setup_routes


if __name__ == "__main__":
    init_db()
    load_data()
    app = web.Application()
    setup_routes(app)
    web.run_app(app, port=8000)
