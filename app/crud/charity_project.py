from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    """
    Класс для операций CRUD с моделью CharityProject.
    """

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
