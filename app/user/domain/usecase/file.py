from abc import ABC, abstractmethod

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
    async def download_file(
        self,
        *,
        file_id: int = None,
        filename: str = None
    ) -> FileResponse:
        """Download file"""
