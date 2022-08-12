import base64
import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        """
        Получение одного пользователя по id
        :param uid:
        :return:
        """
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        """
        получение одного пользователя по username
        :param username:
        :return:
        """
        return self.dao.get_by_username(username)

    def get_all(self):
        """
        получение всех пользователей
        :return:
        """
        return self.dao.get_all()

    def create(self, user_data):
        """
        создание пользователя и генерация хэшированного пароля
        :param user_data:
        :return:
        """
        user_data["password"] = self.generate_password(user_data["password"])
        return self.dao.create(user_data)

    def generate_password(self, password):
        """
        функция хеширования пароля
        :param password:
        :return:
        """
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def update(self, user_data):
        """
        Полное изменение пользователя
        :param user_data:
        :return:
        """
        uid = user_data.get("id")
        user = self.get_one(uid)

        user_data["password"] = self.generate_password(user_data["password"])

        user.username = user_data.get("username")
        user.password = user_data.get("password")
        user.role = user_data.get("role")

        self.dao.update(user)

    def update_partial(self, user_data):
        """
        Частичное изменение пользователя
        :param user_data:
        :return:
        """
        uid = user_data.get("id")
        user = self.get_one(uid)

        if "username" in user_data:
            user.username = user_data.get("username")
        if "password" in user_data:
            user_data["password"] = self.generate_password(user_data["password"])
            user.password = user_data.get("password")
        if "role" in user_data:
            user.role = user_data.get("role")

        self.dao.update(user)

    def delete(self, uid):
        """
        Удаление пользователя
        :param uid:
        :return:
        """
        self.dao.delete(uid)

    def compare_passwords(self, password_hash, password) -> bool:
        """
        Сравнение паролей возвращает True или False
        :param password_hash:
        :param password:
        :return:
        """
        decode_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decode_digest, hash_digest)
