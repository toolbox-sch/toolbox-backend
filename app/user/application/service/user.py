from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO, ChangeUserNicknameRequestDTO
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper
from core.helpers.password import PasswordEncoder
from datetime import datetime


class UserService(UserUseCase):

    def __init__(self, *, repository: UserRepositoryAdapter):
        self.repository = repository

    async def is_admin(self, *, user_id: int) -> bool:
        result = await self.repository.get_user_by_id(user_id=user_id)
        if not result:
            raise UserNotFoundException
        return result.is_admin

    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    @Transactional()
    async def create_user(self, *, command: CreateUserCommand) -> None:
        if command.password1 != command.password2:
            raise PasswordDoesNotMatchException

        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            email=command.email,
            password=PasswordEncoder.encode(command.password1),
            nickname=command.nickname,
        )
        await self.repository.save(user=user)

    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_or_nickname(
            email=email,
            nickname=""
        )

        if not user or user.deleted_at is not None:
            raise UserNotFoundException

        if not PasswordEncoder.matches(password, user.password):
            raise UserNotFoundException

        response = LoginResponseDTO(
            access_token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def modify_nickname(self, *, user_id: int, nickname: str) -> str:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        user.nickname = nickname
        await self.repository.save(user=user)
        return nickname

    @Transactional()
    async def change_password(self, *, user_id: int, password1: str, password2: str) -> None:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        if password1 != password2:
            raise PasswordDoesNotMatchException

        user.password = PasswordEncoder.encode(password1)
        await self.repository.save(user=user)

    @Transactional()
    async def get_user(self, *, user_id) -> UserRead:
        user = await self.repository.get_user_by_id(user_id=user_id)
        return UserRead.model_validate(user)

    @Transactional()
    async def delete_user(self, *, user_id: int) -> None:
        await self.repository.destroy(user_id=user_id)