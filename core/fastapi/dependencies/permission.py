from abc import ABC, abstractmethod
from typing import Type

import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn, HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status

from app.container import Container
from app.user.domain.usecase.user import UserUseCase
from core.exceptions import CustomException
from core.helpers.token import TokenHelper


class UnauthorizedException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = ""


class InvalidTokenException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_TOKEN"
    message = "Invalid token"


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        """has permission"""


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    @inject
    async def has_permission(
        self,
        request: Request,
        usecase: UserUseCase = Depends(Provide[Container.user_service]),
    ) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await usecase.is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(HTTPBearer):
    def __init__(self, permissions: list[Type[BasePermission]]):
        super().__init__(auto_error=False)
        self.permissions = permissions

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise UnauthorizedException

        try:
            payload = TokenHelper.decode(param)
            request.user.id = payload.get("user_id")
        except jwt.PyJWTError:
            raise InvalidTokenException

        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception

    def __hash__(self):
        return hash(tuple(self.permissions))