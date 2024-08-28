from sqlalchemy import String, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class CharityProject(BaseModel):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint(
            'LENGTH(name) >= 1 AND LENGTH(description) >= 1',
            name='check_name_and_description_length'
        ),
    )
