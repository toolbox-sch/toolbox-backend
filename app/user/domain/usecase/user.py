from abc import ABC, abstractmethod
from app.user.application.dto import LoginResponseDTO, ChangeUserNicknameRequestDTO
from app.user.domain.entity.user import User
from app.user.domain.command import CreateUserCommand


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def create_user(self, *, command: CreateUserCommand) -> None:
        """Create User"""

    @abstractmethod
    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        """Login"""

    @abstractmethod
    async def is_admin(self, *, user_id: int) -> bool:
        """Check is admin"""

    @abstractmethod
    async def modify_nickname(self, *, user_id: int, nickname: str) -> str:
        """Modify user"""

    @abstractmethod
    async def change_password(self, *, user_id: int, password1: str, password2: str) -> None:
        """Change password"""

    @abstractmethod
    async def get_user(self, *, user_id) -> User:
        """Get user"""

    @abstractmethod
    async def delete_user(self, *, user_id: int) -> None:
        """Delete user"""
