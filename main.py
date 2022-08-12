from flask import Flask
from flask_restx import Api

from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from config import Config
from setup_db import db


def create_app(config_object):
    """
    Функция для создания App
    :param config_object:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)  # Запись Namespace в app
    api.add_namespace(director_ns)  # Запись Namespace в app
    api.add_namespace(genre_ns)  # Запись Namespace в app
    api.add_namespace(user_ns)  # Запись Namespace в app
    api.add_namespace(auth_ns)  # Запись Namespace в app


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(port=8000, debug=True)
