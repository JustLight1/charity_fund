from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.

    Attributes:
        app_title (str): Название приложения.
        database_url (str): URL базы данных.
        secret (str): Секретный ключ приложения.
        first_superuser_email (EmailStr or None, default = None): Email первого
                                                            суперпользователя.
        first_superuser_password (str or None, default = None): Пароль первого
                                                            суперпользователя.
        model_config (SettingsConfigDict): Конфигурация модели.
    """
    app_title: str
    database_url: str
    secret: str = 'secret'
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
