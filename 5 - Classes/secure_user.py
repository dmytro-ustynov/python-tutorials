import hashlib


class SecureUser:
    def __init__(self, username, password):
        # Захищені атрибути (конвенція Python)
        # Одне підкреслення (_) = "protected" - для внутрішнього використання
        # НЕ справжня приватність! Можна отримати як user._username
        self._username = None               # Захищений атрибут - ім'я користувача
        self._failed_attempts = 0           # Захищений атрибут - кількість невдалих спроб
        self._locked = False                # Захищений атрибут - статус блокування

        # "Приватні" атрибути (name mangling Python)
        # Два підкреслення (__) = "private" - Python змінює назву атрибута
        # Стає user._SecureUser__password_hash замість user.__password_hash
        self.__password_hash = None         # "Приватний" атрибут - хеш пароля
        self.__salt = "security_salt_2024"  # "Приватний" атрибут - сіль для хешування
        self.__max_attempts = 3             # "Приватна" константа - максимум спроб

        # Використовуємо методи для валідації при створенні
        self.set_username(username)
        self.set_password(password)

    def set_username(self, username):
        """Публічний метод - встановлення імені користувача з валідацією"""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Username can only contain letters, numbers, - and _")
        self._username = username

    def get_username(self):
        """Публічний метод - отримання імені користувача"""
        return self._username

    def _validate_password_strength(self, password):
        """ Захищений метод - валідація міцності пароля

        Конвенція: одне підкреслення = метод для внутрішнього використання
        Але все одно доступний як user._validate_password_strength()
        """
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain uppercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain digit")
        if not any(c in "!@#$%^&*" for c in password):
            errors.append("Password must contain special character")

        if errors:
            raise ValueError("; ".join(errors))

    def __generate_hash(self, password):
        """ "Приватний" метод - генерація безпечного хешу

        Два підкреслення = name mangling: стає _SecureUser__generate_hash()
        Python "приховує" цей метод, але все одно можна отримати!
        """
        salted_password = password + self.__salt
        return hashlib.sha256(salted_password.encode()).hexdigest()

    def __reset_security_state(self):
        """ "Приватний" метод - скидання стану безпеки"""
        self._failed_attempts = 0
        self._locked = False
        self.__log_private_event("Security state reset")

    def __log_private_event(self, event):
        """ "Приватний" метод - приватне логування"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[PRIVATE LOG {timestamp}] {self._username}: {event}")

    def set_password(self, password):
        """Публічний метод - встановлення пароля з валідацією та хешуванням"""
        # Використовуємо захищений метод для валідації
        self._validate_password_strength(password)

        # Використовуємо "приватний" метод для генерації хешу
        self.__password_hash = self.__generate_hash(password)

        # Скидаємо стан безпеки при зміні пароля
        self.__reset_security_state()

    def verify_password(self, password):
        """Публічний метод - перевірка пароля з захистом від брут-форсу"""
        if self._locked:
            raise Exception("Account is locked due to too many failed attempts")

        # Використовуємо "приватний" метод для генерації хешу для порівняння
        password_hash = self.__generate_hash(password)

        if self.__password_hash == password_hash:
            self._failed_attempts = 0  # Скидаємо лічильник при успіху
            self.__log_private_event("Successful login")
            return True
        else:
            self._failed_attempts += 1
            if self._failed_attempts >= self.__max_attempts:
                self._locked = True
                self._log_security_event("Account locked due to brute force")
                self.__log_private_event(f"Account locked after {self.__max_attempts} attempts")
            return False

    def _log_security_event(self, event):
        """ Захищений метод - логування подій безпеки

        Внутрішній метод для записування безпекових подій
        Доступний зовні, але порушує конвенцію
        """
        print(f"SECURITY EVENT [{self._username}]: {event}")

    def is_locked(self):
        """Публічний метод - перевірка статусу блокування"""
        return self._locked


# Тестування та демонстрація "приватності" Python
try:
    user = SecureUser("admin", "SecurePass123!")
    print(f"User created: {user.get_username()}")

    # Правильне використання - публічні методи
    print("Correct password:", user.verify_password("SecurePass123!"))

    print("\n=== ДЕМОНСТРАЦІЯ ЗАХИЩЕНИХ (_) АТРИБУТІВ/МЕТОДІВ ===")
    # ️ Порушення конвенції - доступ до "захищених" атрибутів
    print(f"Direct access to 'protected' username: {user._username}")
    print(f"Direct access to 'protected' attempts: {user._failed_attempts}")

    # ️ Виклик "захищеного" методу (порушує конвенцію, але працює)
    user._log_security_event("Manual security event")

    print("\n=== ДЕМОНСТРАЦІЯ 'ПРИВАТНИХ' (__) АТРИБУТІВ/МЕТОДІВ ===")
    # Спроба доступу до "приватних" атрибутів - не працює
    try:
        print(f"Direct access to __password_hash: {user.__password_hash}")
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")

    try:
        print(f"Direct access to __salt: {user.__salt}")
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")

    #  Спроба виклику "приватного" методу - не працює
    try:
        user.__generate_hash("test")
    except AttributeError as e:
        print(f"❌ AttributeError calling __generate_hash: {e}")

    print("\n=== АЛЕ! NAME MANGLING МОЖНА ОБІЙТИ ===")
    #  Python змінює назви, але їх все одно можна отримати!
    print("Name mangling creates these attributes:")
    private_attrs = [attr for attr in dir(user) if 'SecureUser__' in attr]
    for attr in private_attrs:
        print(f"  - {attr}")

    #  Доступ через name mangling
    print(f"'Private' salt via name mangling: {user._SecureUser__salt}")
    print(f"'Private' max attempts: {user._SecureUser__max_attempts}")

    # Виклик "приватного" методу через name mangling
    test_hash = user._SecureUser__generate_hash("test_password")
    print(f"'Private' method result: {test_hash[:20]}...")

    # Можна навіть змінити "приватні" дані!
    print(f"Max attempts before: {user._SecureUser__max_attempts}")
    user._SecureUser__max_attempts = 10  # Змінюємо "приватну" константу
    print(f"Max attempts after modification: {user._SecureUser__max_attempts}")

    print("\n=== ВАЖЛИВА ПРИМІТКА ===")
    print("Python НЕ має справжньої приватності!")
    print("• _attribute - 'захищений' (конвенція, легко доступний)")
    print("• __attribute - 'приватний' (name mangling, складніше, але доступний)")
    print("• Це філософія Python: 'Ми всі дорослі люди' (We're all consenting adults)")
    print("• Для справжньої безпеки використовуйте правильну авторизацію на рівні додатка!")

except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Security error: {e}")
