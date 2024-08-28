from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Donation(BaseModel):
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('user.id'))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
