from abc import ABC, abstractmethod
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse


class FileUseCase(ABC):
    @abstractmethod
    async def upload_file(
        self,
        *,
        file: UploadFile
    ) -> str:
        """Upload file"""

    @abstractmethod
    async def upload_files(
        self,
        *,
        files: List[UploadFile]
    ):
        """Upload files"""

    @abstractmethod
    async def download_file(
        self,
        *,
        filename: str
    ) -> FileResponse:
        """Download file"""
