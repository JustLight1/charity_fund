from datetime import datetime

from sqlalchemy import Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    )

    @validates('fully_invested')
    def validate_fully_invested(self, key, value):
        if value:
            if self.close_date is None:
                self.close_date = datetime.now()
        return value
