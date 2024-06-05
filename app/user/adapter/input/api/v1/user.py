from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request

from app.container import Container
from app.user.adapter.input.api.v1.request import CreateUserRequest, LoginRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import (
    CreateUserResponseDTO,
    GetUserResponseDTO,
    ChangeUserNicknameRequestDTO,
    ChangePasswordRequestDTO
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import IsAdmin, PermissionDependency, IsAuthenticated

user_router = APIRouter()


@user_router.get(
    "/me",
    response_model=GetUserResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_user(
    request: Request,
    usecase: UserUseCase = Depends(Provide[Container.user_service])
):
    return await usecase.get_user(user_id=request.user.id)


@user_router.get(
    "s",
    response_model=list[GetUserResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
@inject
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    return await usecase.get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
@inject
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    command = CreateUserCommand(**request.model_dump())
    await usecase.create_user(command=command)
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
@inject
async def login(
    request: LoginRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    token = await usecase.login(email=request.email, password=request.password)
    return {"accessToken": token.access_token, "refreshToken": token.refresh_token}


@user_router.patch(
    "/nickname",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def modify_nickname(
    request: Request,
    body: ChangeUserNicknameRequestDTO,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    nickname = await usecase.modify_nickname(
        user_id=request.user.id, nickname=body.nickname
    )

    return {"nickname": nickname}


@user_router.patch(
    "/password",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def change_password(
    request: Request,
    body: ChangePasswordRequestDTO,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    await usecase.change_password(
        user_id=request.user.id,
        password1=body.password1,
        password2=body.password2,
    )
    return {}


@user_router.delete(
    "",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def withdrawal(
    request: Request,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    await usecase.delete_user(user_id=request.user.id)
    return {}
