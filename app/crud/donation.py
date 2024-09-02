from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate
from app.services.investment import investment


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    BaseModel
]):
    """
    Класс для операций CRUD с моделью Donation.
    """

    async def create(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User | None = None
    ) -> Donation:
        """
        Создает новое пожертвование и запускает инвестиционный процесс.

        Args:
            obj_in (DonationCreate): Данные для создания пожертвования.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User or None): Пользователь, создающий пожертвование.

        Returns:
            Donation: Созданное пожертвование.
        """
        donation = await super().create(obj_in, session, user)
        await investment(session)
        await session.refresh(donation)
        return donation

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        """
        Получает все пожертвования, сделанные пользователем.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User): Пользователь, чьи пожертвования нужно получить.

        Returns:
            list[Donation]: Список пожертвований.
        """
        donations = await session.scalars(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.all()


donation_crud = CRUDDonation(Donation)
