import os
import uuid

from io import BytesIO
from typing import List
from fastapi import UploadFile
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

from app.user.domain.entity.user_file import UserFile
from core.db import Transactional
from core.exceptions import CustomException

from app.user.adapter.output.persistence.repository_adapter import UserFileRepositoryAdapter
from app.user.domain.usecase.tool import ToolUseCase

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_PATH, "..", "..", "static/")


# Decorator to create data
def save(f):
    async def wrapper(*args, **kwargs):
        filename = await f(*args, **kwargs)
        user_file = UserFile.create(name=filename, user_id=kwargs["user_id"])
        await args[0].repository.save(user_file=user_file)
        return filename
    return wrapper


class ToolService(ToolUseCase):
    def __init__(self, *, repository: UserFileRepositoryAdapter):
        self.repository = repository

    @Transactional()
    @save
    async def merge_pdf(self, *, files: List[UploadFile], user_id: int) -> str:
        if not files:
            raise CustomException("No PDFs to merge")
        else:
            merger = PdfWriter()

            for file in files:
                merger.append(PdfReader(file.file))

            merged_name = f"/{str(uuid.uuid4())}.pdf"
            merger.write(FILE_PATH + merged_name)

        return merged_name

    @Transactional()
    @save
    async def split_pdf(self, *, file: UploadFile, start: int, end: int, user_id: int) -> str:
        pdf = PdfReader(file.file)
        writer = PdfWriter()

        for page in range(start - 1, end):
            writer.add_page(pdf.pages[page])

        split_name = f"/{str(uuid.uuid4())}.pdf"
        writer.write(FILE_PATH + split_name)

        return split_name

    @Transactional()
    @save
    async def encrypt_pdf(self, *, file: UploadFile, key: str, user_id: int) -> str:
        pdf = PdfReader(file.file)
        writer = PdfWriter()

        for page in pdf.pages:
            writer.add_page(page)

        encrypted_name = f"/{str(uuid.uuid4())}.pdf"
        writer.encrypt(key)
        writer.write(FILE_PATH + encrypted_name)

        return encrypted_name

    @Transactional()
    @save
    async def extract_pdf_text(self, *, file: UploadFile, user_id: int) -> str:
        pdf = PdfReader(file.file)
        text = ""

        for page in pdf.pages:
            text += page.extract_text()

        return text

    @Transactional()
    async def pdf_to_png(self, *, file: UploadFile, user_id: int) -> List[str]:
        pdf = convert_from_bytes(file.file.read())
        image_names = []
        converted_name = f"/{str(uuid.uuid4())}"

        for i, image in enumerate(pdf):
            image_name = f"{converted_name}_{i}.png"
            image.save(os.path.join(FILE_PATH, image_name), "PNG")
            image_names.append(image_name)

        for filename in image_names:
            user_file = UserFile.create(name=filename, user_id=user_id)
            await self.repository.save(user_file=user_file)

        return image_names

    @Transactional()
    @save
    async def convert_image(self, *, file: UploadFile, target: str, user_id: int):
        target_format = target.upper()
        if target_format not in ["PNG", "JPG", "ICO", "WEBP"]:
            raise CustomException("Invalid file format")

        try:
            # image = Image.open(os.path.join(FILE_PATH, file.filename))
            image = Image.open(file.file)
            converted_image = BytesIO()
            image.convert("RGB").save(converted_image, format=target_format)

            converted_name = f"{str(uuid.uuid4())}.{target_format.lower()}"

            with open(os.path.join(FILE_PATH, converted_name), "wb") as f:
                f.write(converted_image.getvalue())

        except Exception as e:
            raise CustomException("Error converting image") from e

        return converted_name
