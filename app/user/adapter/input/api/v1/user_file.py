from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.user.application.dto import GetFileResponseDTO
from app.user.domain.usecase.user_file import UserFileUseCase
from core.fastapi.dependencies import PermissionDependency, IsAdmin

user_file_router = APIRouter()


@user_file_router.get(
    "/{file_id}",
    response_model=GetFileResponseDTO,
)
@inject
async def get_file(
    file_id: int,
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    return await usecase.get_file(file_id=file_id)


@user_file_router.get(
    "s",
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
    "/{file_id}",
)
@inject
async def delete_file(
    file_id: int,
    usecase: UserFileUseCase = Depends(Provide[Container.user_file_service])
):
    await usecase.destroy(file_id=file_id)
    return {}
