from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class UserFile(Base, TimestampMixin):
    __tablename__ = "user_file"

    file_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    extension: Mapped[str] = mapped_column(String(10), nullable=False)
    path: Mapped[str] = mapped_column(String(100), nullable=False)

    user = relationship("User", back_populates="user_files")

    @classmethod
    def create(
        cls, *, user_id: int, name: str, extension: str, path: str
    ) -> "UserFile":
        return cls(
            user_id=user_id,
            name=name,
            extension=extension,
            path=path
        )


class UserFileRead(BaseModel):
    file_id: int = Field(..., title="File ID")
    name: str = Field(..., title="Name")
    extension: str = Field(..., title="Extension")
    path: str = Field(..., title="Path")
    created_at: datetime = Field(..., title="Created At")
