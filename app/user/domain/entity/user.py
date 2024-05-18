from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.user.domain.vo.location import Location
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    @classmethod
    def create(
        cls, *, email: str, password: str, nickname: str
    ) -> "User":
        return cls(
            email=email,
            password=password,
            nickname=nickname
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")
