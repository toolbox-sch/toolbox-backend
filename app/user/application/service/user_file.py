from fastapi import UploadFile

from app.user.adapter.output.persistence.repository_adapter import UserFileRepositoryAdapter
from app.user.domain.entity.user_file import UserFile, UserFileRead
from app.user.domain.usecase.user_file import UserFileUseCase
from core.db import Transactional


class UserFileService(UserFileUseCase):
    def __init__(self, repository: UserFileRepositoryAdapter):
        self.repository = repository

    async def get_file(
            self,
            *,
            file_id: int
    ) -> UserFileRead:
        file = await self.repository.get_file(file_id=file_id)
        return UserFileRead.model_validate(file)

    async def get_files(
            self,
            *,
            limit: int = 12,
            prev: int | None = None
    ) -> list[UserFileRead]:
        return await self.repository.get_files(limit=limit, prev=prev)

    @Transactional()
    async def destroy(self, *, file_id: int) -> None:
        await self.repository.destroy(file_id=file_id)
