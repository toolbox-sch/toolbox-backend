from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, UploadFile, File, Depends

from app.container import Container
from app.user.domain.usecase.file import FileUseCase
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated

file_router = APIRouter()


@file_router.post(
    "/upload",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def upload_file(
    request: UploadFile = File(...),
    usecase: FileUseCase = Depends(Provide[Container.file_service])
):
    await usecase.upload_file(file=request)


@file_router.get(
    "/download/{filename}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def download_file(
    filename: str,
    usecase: FileUseCase = Depends(Provide[Container.file_service])
):
    return await usecase.download_file(filename=filename)
