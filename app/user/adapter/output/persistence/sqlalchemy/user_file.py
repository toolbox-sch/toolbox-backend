from app.user.domain.entity.user_file import UserFile
from app.user.domain.repository.user_file import UserFileRepo
from sqlalchemy import select, and_, or_

from core.db import session_factory


class UserFileSQLAlchemyRepo(UserFileRepo):
    async def get_file(
            self,
            *,
            file_id: int
    ) -> UserFile:
        query = select(UserFile).where(UserFile.file_id == file_id)

        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().first()

    async def get_files(
            self,
            *,
            limit: int = 12,
            prev: int | None = None
    ) -> list[UserFile]:
        query = select(UserFile).order_by(UserFile.file_id.desc())

        if prev:
            query = query.where(UserFile.file_id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().all()
