import os
import uuid
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.user.adapter.output.persistence.repository_adapter import UserFileRepositoryAdapter
from app.user.application.exception import NullFileException, RejectFileCreationException
from app.user.domain.usecase.file import FileUseCase

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_PATH, "..", "..", "static/")


def get_extension(filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return extension


class FileService(FileUseCase):

    def __init__(self, *, repository: UserFileRepositoryAdapter):
        self.repository = repository

    async def upload_file(self, *, file: UploadFile) -> str:
        if not file:
            raise NullFileException

        filename = f"{str(uuid.uuid4())}.{get_extension(file.filename)}"

        try:
            with open(os.path.join(FILE_PATH, filename), "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            raise RejectFileCreationException from e

        return filename

    async def upload_files(self, *, files: List[UploadFile]) -> List[str]:
        filenames = []
        if not files:
            raise NullFileException

        for file in files:
            filename = f"{str(uuid.uuid4())}.{get_extension(file.filename)}"

            try:
                with open(os.path.join(FILE_PATH, filename), "wb") as f:
                    f.write(file.file.read())
            except Exception as e:
                raise RejectFileCreationException from e

            filenames.append(filename)

        return filenames

    async def download_file(self, *, filename: str) -> FileResponse:
        if filename is None:
            raise NullFileException

        return FileResponse(f"{FILE_PATH}{filename}", filename=filename)
