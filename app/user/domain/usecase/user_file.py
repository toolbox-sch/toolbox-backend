from abc import ABC, abstractmethod

from app.user.domain.entity.user_file import UserFile, UserFileRead


class UserFileUseCase(ABC):
    @abstractmethod
    async def get_file(self, *, file_id: int) -> UserFileRead:
        """ Get file by id """

    @abstractmethod
    async def get_files(self, *, limit: int = 12, prev: int | None = None) -> list[UserFileRead]:
        """ Get files list """

    @abstractmethod
    async def get_user_files(self, *, user_id: int) -> list[UserFileRead]:
        """ Get user files """

    @abstractmethod
    async def destroy(self, *, file_id: int) -> None:
        """ Delete file """
