from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для операций CRUD.

    Attributes:
        model (Type[ModelType]): Модель базы данных.
    """

    def __init__(
        self,
        model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> ModelType | None:
        """
        Получает объект по его идентификатору.

        Args:
            obj_id (int): Идентификатор объекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            ModelType or None: Найденный объект или None, если не найден.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> list[ModelType]:
        """
        Получает список всех объектов модели.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[ModelType]: Список всех объектов модели.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: User | None = None,
    ) -> ModelType:
        """
        Создает новый объект модели в базе данных.

        Args:
            obj_in (CreateSchemaType): Данные для создания объекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User or None, default= None): Пользователь, создающий объект.

        Returns:
            ModelType: Созданный объект модели.
        """
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        """
        Обновляет существующий объект модели в базе данных.

        Args:
            db_obj (ModelType): Существующий объект модели.
            obj_in (UpdateSchemaType): Новые данные для обновления.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            ModelType: Обновленный объект модели.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """
        Удаляет объект модели из базы данных.

        Args:
            db_obj (ModelType): Объект модели для удаления.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            ModelType: Удаленный объект модели.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
