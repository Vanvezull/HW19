from flask import request
from flask_restx import Namespace, Resource

from container import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """
        Генерация токенов для пользователя
        :return:
        """
        data = request.json

        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return "", 400
        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        """
        Генерация Access токена при наличии Refresh токена
        :return:
        """
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
