from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя.

    Inherits:
        Base: Базовый класс для всех моделей.
        Attributes:
            __tablename__ (str): Имя таблицы, устанавливается как имя класса
                                в нижнем регистре.
            id (Mapped[int]): Первичный ключ.

    По умолчанию содержит следующие поля:
        id (int) - Идентификатор пользователя.
        email (str) - Адрес электронной почты пользователя.
        pasword (str) - Пароль пользователя.
        is_active (bool) - Активен ли пользователь (True по умолчанию).
        is_verified (bool) - Подтверждён ли пользователь (False по умолчанию).
        is_superuser (bool) - Есть ли у пользователя права
                              «суперюзера» (False по умолчанию).
    """
    pass
