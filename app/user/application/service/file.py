import os
import uuid

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.user.adapter.output.persistence.repository_adapter import UserFileRepositoryAdapter
from app.user.application.exception import NullFileException, RejectFileCreationException
from app.user.domain.usecase.file import FileUseCase

FILE_PATH = "app/user/static/"


class FileService(FileUseCase):

    def __init__(self, *, repository: UserFileRepositoryAdapter):
        self.repository = repository

    async def upload_file(self, *, file: UploadFile) -> str:
        if file is None:
            raise NullFileException

        filename = f"{str(uuid.uuid4())}"

        try:
            with open(os.path.join(FILE_PATH, filename), "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            raise RejectFileCreationException from e

        return filename

    async def download_file(self, *, file_id: int = None, filename: str = None) -> FileResponse:
        if file_id is not None:
            file = await self.repository.get_file(file_id=file_id)
            filename = file.name

        return FileResponse(f"{FILE_PATH}{filename}", filename=filename)
