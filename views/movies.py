from flask import request
from flask_restx import Namespace, Resource

from container import movie_service
from dao.models.movie import MoviesSchema
from helpers.decorators import auth_required, admin_required

"""
Вьюшки и namecspace для Movie
"""

movie_ns = Namespace('movies')


@movie_ns.route('/')  # Представление для получения всех фильмов, а так же фильмов по директору и жанру
class MoviesView(Resource):
    @auth_required
    def get(self):
        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id', type=int)
        year = request.args.get('year', type=int)

        filters = {
            "director_id": director_id,
            "genre_id": genre_id,
            "year": year
        }

        movies = movie_service.get_all(filters)

        return MoviesSchema(many=True).dump(movies), 200

    @admin_required
    def post(self):
        req_json = request.json
        movie_service.create(req_json)

        return "", 201


@movie_ns.route('/<int:id>')  # Представление для получения фильма по id
class MovieView(Resource):
    @auth_required
    def get(self, id):
        movie = movie_service.get_one(id)
        return MoviesSchema().dump(movie), 201, {"location": f"/movies/{movie.id}"}

    @admin_required
    def put(self, id):
        req_json = request.json
        req_json["id"] = id

        movie_service.update(req_json)
        return "", 204

    @admin_required
    def patch(self, id):
        req_json = request.json
        req_json["id"] = id

        movie_service.update_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, id):
        movie_service.delete(id)
        return "", 204
