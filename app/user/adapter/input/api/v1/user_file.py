from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.user.application.dto import GetFileResponseDTO
from app.user.domain.entity.user_file import UserFileRead
from app.user.domain.usecase.user_file import UserFileUseCase
from core.fastapi.dependencies import PermissionDependency, IsAdmin, IsAuthenticated

user_file_router = APIRouter()


@user_file_router.get(
    "/file/{file_id}",
    response_model=GetFileResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_file(
    file_id: int,
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    return await usecase.get_file(file_id=file_id)


@user_file_router.get(
    "/files",
    response_model=list[GetFileResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
@inject
async def get_files(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    return await usecase.get_files(limit=limit, prev=prev)


@user_file_router.delete(
    "/file/{file_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_file(
    file_id: int,
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    await usecase.destroy(file_id=file_id)
    return {}


@user_file_router.get(
    "/{user_id}/files",
    response_model=list[UserFileRead],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_user_files(
    user_id: int,
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    return await usecase.get_user_files(user_id=user_id)
