from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.vo.location import Location
from core.db import Base
from core.db.mixins import TimestampMixin
from datetime import datetime


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    user_files = relationship("UserFile", back_populates="user")

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
    created_at: datetime = Field(..., title="Created At")
