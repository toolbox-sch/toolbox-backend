from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str


class CreateFileCommand(BaseModel):
    name: str
    extension: str
    path: str
    size: int
