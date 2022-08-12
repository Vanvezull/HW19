from flask import request
from flask_restx import Namespace, Resource

from container import genre_service
from dao.models.genre import GenresSchema
from helpers.decorators import auth_required, admin_required

"""
Вьюшки и namespace для Genre
"""

genre_ns = Namespace('genres')


@genre_ns.route('/')  # Представление для получения всех жанров
class GenreView(Resource):
    @auth_required
    def get(self):
        genres = genre_service.get_all()
        return GenresSchema(many=True).dump(genres), 200

    @admin_required
    def post(self):
        req_json = request.json
        genre_service.create(req_json)

        return "", 201


@genre_ns.route('/<int:id>')  # Представление для получения жанра по id
class GenreView(Resource):
    @auth_required
    def get(self, id):
        genre = genre_service.get_one(id)
        return GenresSchema().dump(genre), 201, {"location": f"/genre/{genre.id}"}

    @admin_required
    def put(self, id):
        req_json = request.json
        req_json["id"] = id

        genre_service.update(req_json)
        return "", 204

    @admin_required
    def patch(self, id):
        req_json = request.json
        req_json["id"] = id

        genre_service.update_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, id):
        genre_service.delete(id)
        return ""
