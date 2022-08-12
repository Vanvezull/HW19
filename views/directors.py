from flask import request
from flask_restx import Namespace, Resource

from container import director_service
from dao.models.director import DirectorsSchema
from helpers.decorators import auth_required, admin_required

"""
Вьюшки и namespace для Director
"""

director_ns = Namespace('directors')


@director_ns.route('/')  # Представление для получения всех режиссеров
class DirectorView(Resource):
    @auth_required
    def get(self):
        directors = director_service.get_all()

        return DirectorsSchema(many=True).dump(directors), 200

    @admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)

        return "", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:id>')  # Представление для получения режиссера по id
class DirectorView(Resource):
    @auth_required
    def get(self, id):
        director = director_service.get_one(id)

        return DirectorsSchema().dump(director), 201

    @admin_required
    def put(self, id):
        req_json = request.json
        req_json["id"] = id

        director_service.update(req_json)

        return "", 204

    @admin_required
    def patch(self, id):
        req_json = request.json
        req_json["id"] = id

        director_service.update_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, id):
        director_service.delete(id)

        return "", 204
