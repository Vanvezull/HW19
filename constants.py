# этот файл для глобальных констант. чтобы не хардкодить строки/числа в коде, выносите их сюда.
# например вместо C:\\Windows в коде, создайте константу WINDOWS_PATH здесь и присвойте ей значение

# Пример

JWT_SECRET = 'password'
JWT_ALGO = 'HS256'

PWD_HASH_SALT = b'blitzcrank hook'
PWD_HASH_ITERATIONS = 100_000