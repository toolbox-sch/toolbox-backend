from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from datetime import datetime


class GetUserResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")
    created_at: datetime = Field(..., description="Created at")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    nickname: str = Field(..., description="Nickname")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class LoginResponseDTO(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


# Field default -> None == Optional / Optional Modify DTO
class ChangeUserNicknameRequestDTO(BaseModel):
    email: str = Field(None, description="Email")
    nickname: str = Field(None, description="Nickname")


class ChangePasswordRequestDTO(BaseModel):
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")


class GetFileResponseDTO(BaseModel):
    file_id: int = Field(..., description="ID")
    name: str = Field(..., description="Name")
    created_at: datetime = Field(..., description="Created at")


class DownloadFileRequestDTO(BaseModel):
    filename: str = Field(None, description="File ID")


class PdfSplitterRequestDTO(BaseModel):
    start: int = Field(..., description="Start Page")
    end: int = Field(..., description="End Page")


class ConvertImageRequestDTO(BaseModel):
    file: UploadFile = File(..., description="Image File")
    target: str = Field(..., description="Target Format")
