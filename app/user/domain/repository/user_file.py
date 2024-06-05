from abc import ABC, abstractmethod

from app.user.domain.entity.user_file import UserFile


class UserFileRepo(ABC):
    @abstractmethod
    async def get_file(
            self,
            *,
            file_id: int
    ) -> UserFile:
        """ Get file by id """

    @abstractmethod
    async def get_files(
            self,
            *,
            limit: int = 12,
            prev: int | None = None
    ) -> list[UserFile]:
        """ Get files list """

    @abstractmethod
    async def get_user_files(
            self,
            *,
            user_id: int
    ) -> list[UserFile]:
        """ Get user files """

    @abstractmethod
    async def save(
            self,
            *,
            user_file: UserFile
    ) -> None:
        """ Save file """
