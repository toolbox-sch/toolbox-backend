from abc import ABC, abstractmethod
from typing import List

from fastapi import UploadFile


class ToolUseCase(ABC):
    @abstractmethod
    async def merge_pdf(
        self,
        *,
        files: List[UploadFile],
        user_id: int
    ) -> str:
        """Merge PDF"""

    @abstractmethod
    async def split_pdf(
        self,
        *,
        file: UploadFile,
        start: int,
        end: int,
        user_id: int
    ) -> str:
        """Split PDF"""

    @abstractmethod
    async def encrypt_pdf(
        self,
        *,
        file: UploadFile,
        key: str,
        user_id: int
    ) -> str:
        """Encrypt PDF"""

    @abstractmethod
    async def extract_pdf_text(
        self,
        *,
        file: UploadFile,
        user_id: int
    ) -> str:
        """Extract PDF text"""

    @abstractmethod
    async def pdf_to_png(
        self,
        *,
        file: UploadFile,
        user_id: int
    ) -> List[str]:
        """Convert PDF to PNG"""

    @abstractmethod
    async def convert_image(
        self,
        *,
        file: UploadFile,
        target: str,
        user_id: int
    ):
        """Convert image"""
