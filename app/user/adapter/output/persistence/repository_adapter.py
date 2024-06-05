from datetime import datetime

from app.user.domain.entity.user import User, UserRead
from app.user.domain.entity.user_file import UserFile, UserFileRead
from app.user.domain.repository.user import UserRepo
from app.user.domain.repository.user_file import UserFileRepo


class UserRepositoryAdapter:
    def __init__(self, *, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        users = await self.user_repo.get_users(limit=limit, prev=prev)
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        return await self.user_repo.get_user_by_email_or_nickname(
            email=email,
            nickname=nickname,
        )

    async def get_user_by_id(self, *, user_id: int) -> User | None:
        return await self.user_repo.get_user_by_id(user_id=user_id)

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        return await self.user_repo.get_user_by_email_and_password(
            email=email,
            password=password,
        )

    async def save(self, *, user: User) -> None:
        await self.user_repo.save(user=user)

    async def destroy(self, *, user_id: int) -> None:
        result = await self.user_repo.get_user_by_id(user_id=user_id)
        result.deleted_at = datetime.now()
        await self.user_repo.save(user=result)


class UserFileRepositoryAdapter:
    def __init__(self, *, user_file_repo: UserFileRepo):
        self.user_file_repo = user_file_repo

    async def get_file(self, *, file_id: int) -> UserFile:
        return await self.user_file_repo.get_file(file_id=file_id)

    async def get_files(self, *, limit: int = 12, prev: int | None = None) -> list[UserFileRead]:
        files = await self.user_file_repo.get_files(limit=limit, prev=prev)
        return [UserFileRead.model_validate(file) for file in files]

    async def get_user_files(self, *, user_id: int) -> list[UserFileRead]:
        files = await self.user_file_repo.get_user_files(user_id=user_id)
        return [UserFileRead.model_validate(file) for file in files]

    async def save(self, *, user_file: UserFile) -> None:
        await self.user_file_repo.save(user_file=user_file)

    async def destroy(self, *, file_id: int) -> None:
        result = await self.user_file_repo.get_file(file_id=file_id)
        result.deleted_at = datetime.now()
        await self.user_file_repo.save(user_file=result)
