from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject, Donation


async def investment(session: AsyncSession) -> None:
    """
    Функция распределения инвестиций.
    """
    projects_result = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(CharityProject.create_date)
    )
    projects = projects_result.scalars().all()

    donations_result = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(Donation.create_date)
    )
    donations = donations_result.scalars().all()

    project_index = 0
    donation_index = 0

    while project_index < len(projects) and donation_index < len(donations):
        project = projects[project_index]
        donation = donations[donation_index]

        available_project_amount = (
            project.full_amount - project.invested_amount
        )
        available_donation_amount = (
            donation.full_amount - donation.invested_amount
        )

        amount_to_invest = min(available_project_amount,
                               available_donation_amount)

        project.invested_amount += amount_to_invest
        donation.invested_amount += amount_to_invest

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now(timezone.utc)
            project_index += 1

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now(timezone.utc)
            donation_index += 1

        # Если ни проект, ни пожертвование не закрыты, продолжаем с текущими
        if available_project_amount > available_donation_amount:
            donation_index += 1
        elif available_project_amount < available_donation_amount:
            project_index += 1
        else:
            project_index += 1
            donation_index += 1

    await session.commit()
