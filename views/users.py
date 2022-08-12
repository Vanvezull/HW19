from flask import request
from flask_restx import Namespace, Resource

from container import user_service
from dao.models.user import UserSchema
from helpers.decorators import admin_required, auth_required
"""
Вьюшки и Namespace для пользователей
"""

user_ns = Namespace('users')


@user_ns.route('/')  # Представление для получения всех пользователей
class UserView(Resource):
    @auth_required
    def get(self):
        users = user_service.get_all()

        return UserSchema(many=True).dump(users), 200

    @admin_required
    def post(self):
        req_json = request.json
        user = user_service.create(req_json)

        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:id>')  # Представление для получения пользователя по id
class UserView(Resource):
    @auth_required
    def get(self, id):
        user = user_service.get_one(id)

        return UserSchema().dump(user), 201

    @admin_required
    def put(self, id):
        req_json = request.json
        req_json["id"] = id

        user_service.update(req_json)

        return "", 204

    @admin_required
    def patch(self, id):
        req_json = request.json
        req_json["id"] = id

        user_service.update_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, id):
        user_service.delete(id)

        return "", 204
