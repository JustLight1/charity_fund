from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """
    Базовая схема благотворительного проекта.

    Attributes:
        name (str or None): Имя проекта.
        description (str or None): Описание проекта.
        full_amount (PositiveInt or None): Сумма взноса.
        model_config (ConfigDict): Конфигурация модели для запрета
        дополнительных полей при валидации.
    """
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1)
    full_amount: PositiveInt | None = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    """
    Схема для создания нового благотворительного проекта.

    Attributes:
        name (str): Имя переговорной комнаты.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема для обновления благотворительного проекта.
    """


class CharityProjectDB(CharityProjectCreate):
    """
    Схема благотворительного проекта в базе данных.

    Inherits:
        CharityProjectCreate: Схема для создания нового благотворительного
        проекта.

    Attributes:
        id (int): Идентификатор благотворительного проекта.
        invested_amount (int): Сумма, уже вложенная в проект.
        fully_invested (bool): Флаг, указывающий, полностью ли профинансирован
        проект.
        create_date (dt.datetime): Дата создания проекта.
        close_date (dt.datetime): Дата закрытия проекта (если применимо).
        model_config (ConfigDict): Конфигурация схемы для сериализации объектов
        базы данных, а не только Python-словарь или JSON-объект.
    """
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
