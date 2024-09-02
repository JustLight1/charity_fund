from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.services.investment import investment


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    """
    Класс для операций CRUD с моделью CharityProject.
    """

    async def create(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
        user: User | None = None
    ) -> CharityProject:
        """
        Создает новый проект и запускает инвестиционный процесс.

        Args:
            obj_in (CharityProjectCreate): Данные для создания проекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User or None): Пользователь, создающий проект.

        Returns:
            CharityProject: Созданный проект.
        """
        project = await super().create(obj_in, session, user)
        await investment(session)
        await session.refresh(project)
        return project

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> int | None:
        """
        Получает идентификатор проекта по его названию.

        Args:
            project_name (str): Название проекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            int or None: Идентификатор найденного проекта или None,
                         если проект не найден.
        """
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
