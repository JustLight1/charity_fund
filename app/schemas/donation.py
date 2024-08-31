from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt


class DonationBase(BaseModel):
    """
    Базовая схема для пожертвования.

    Attributes:
        full_amount (int): Сумма пожертвования.
        comment (str or None): Комментарий к пожертвованию.
        model_config (ConfigDict): Конфигурация модели для запрета
        дополнительных полей при валидации.
    """
    full_amount: PositiveInt = None
    comment: str | None = None

    model_config = ConfigDict(extra='forbid')


class DonationCreate(DonationBase):
    """
    Схема для создания пожертвования.
    """
    full_amount: PositiveInt


class DonationUpdate(BaseModel):
    """
    Схема пожертвования для обновления.
    """
    pass


class DonationDB(DonationCreate):
    """
    Схема пожертвования в базе данных.

    Attributes:
        id (int): Идентификатор пожертвования.
        create_date (dt.datetime): Дата создания пожертвования.
        user_id (int): ID пользователя, сделавшего пожертвование.
        invested_amount (int): Сумма, вложенная из пожертвования.
        fully_invested (bool): Флаг, указывающий, полностью ли вложено
        пожертвование.
        close_date (datetime or None): Дата закрытия пожертвования
        (если применимо).
        model_config (ConfigDict): Конфигурация схемы для сериализации объектов
        базы данных, а не только Python-словарь или JSON-объект.
    """
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
