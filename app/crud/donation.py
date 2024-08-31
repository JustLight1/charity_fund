from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):
    """
    Класс для операций CRUD с моделью Donation.
    """

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
