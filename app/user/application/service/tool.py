import os
import uuid
from io import BytesIO

from typing import List
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from pdf2image import convert_from_path

from core.exceptions import CustomException

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_PATH, "..", "..", "static/")


class PdfTools:
    @staticmethod
    def merger(*, files: List[str]) -> str:
        filenames = [os.path.join(FILE_PATH, file) for file in files]

        if not filenames:
            raise CustomException("No PDFs to merge")
        else:
            merger = PdfWriter()
            for filename in filenames:
                merger.append(PdfReader(open(filename, "rb")))

            merged_name = str(uuid.uuid4())
            merger.write(FILE_PATH + f"/{merged_name}.pdf")

        return merged_name

    @staticmethod
    def get_pages(*, file: str) -> int:
        pdf = PdfReader(open(os.path.join(FILE_PATH, file), "rb"))
        return len(pdf.pages)

    @staticmethod
    def splitter(*, file: str, start: int, end: int) -> str:
        pdf = PdfReader(open(os.path.join(FILE_PATH, file), "rb"))
        writer = PdfWriter()

        for page in range(start - 1, end):
            writer.add_page(pdf.pages[page])

        split_name = str(uuid.uuid4())
        writer.write(FILE_PATH + f"/{split_name}.pdf")

        return split_name

    @staticmethod
    def encrypt(*, file: str, password: str) -> str:
        pdf = PdfReader(open(os.path.join(FILE_PATH, file), "rb"))
        writer = PdfWriter()

        for page in pdf.pages:
            writer.add_page(page)

        encrypted_name = str(uuid.uuid4())
        writer.encrypt(password)
        writer.write(FILE_PATH + f"/{encrypted_name}.pdf")

        return encrypted_name

    @staticmethod
    def extract_text(*, file: str) -> str:
        pdf = PdfReader(open(os.path.join(FILE_PATH, file), "rb"))
        text = ""

        for page in pdf.pages:
            text += page.extract_text()

        return text

    @staticmethod
    def extract_images(*, file: str) -> List[str]:
        pdf = convert_from_path(os.path.join(FILE_PATH, file))
        image_names = []

        for i, image in enumerate(pdf):
            image_name = f"{file}_{i}.png"
            image.save(os.path.join(FILE_PATH, image_name), "PNG")
            image_names.append(image_name)

        return image_names


class ImageTools:
    @staticmethod
    def convert(*, file: str, target_format: str) -> str:
        target_format = target_format.upper()
        if target_format not in ["PNG", "JPG", "ICO", "WEBP"]:
            raise CustomException("Invalid file format")

        try:
            image = Image.open(os.path.join(FILE_PATH, file))
            converted_image = BytesIO()
            image.convert("RGB").save(converted_image, format=target_format)

            converted_name = f"{str(uuid.uuid4())}.{target_format.lower()}"

            with open(os.path.join(FILE_PATH, converted_name), "wb") as f:
                f.write(converted_image.getvalue())

        except Exception as e:
            raise CustomException("Error converting image") from e

        return converted_name
