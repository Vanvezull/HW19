import calendar
import datetime
import jwt
from flask_restx import abort

from services.user import UserService
from constants import JWT_SECRET, JWT_ALGO


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        """
        Генерация новых токенов, а так же пары токенов при окончании времени Access токена
        :param username:
        :param password:
        :param is_refresh:
        :return:
        """

        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        min60 = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data["exp"] = calendar.timegm(min60.timetuple())
        access_token = jwt.encode(data, key=JWT_SECRET, algorithm=JWT_ALGO)

        days120 = datetime.datetime.utcnow() + datetime.timedelta(days=120)
        data["exp"] = calendar.timegm(days120.timetuple())
        refresh_token = jwt.encode(data, key=JWT_SECRET, algorithm=JWT_ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def check_token(self, token):
        """
        Проверка токена, не используется в проекте, было в уроке поэтому и добавил)
        :param token:
        :return:
        """
        try:
            jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGO])
            return True
        except Exception:
            return False

    def approve_refresh_token(self, refresh_token):
        """
        Проверка есть ли Refresh токен
        :param refresh_token:
        :return:
        """
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGO])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)
