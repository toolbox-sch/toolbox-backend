from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, UploadFile, File, Depends

from app.container import Container
from app.user.domain.usecase.file import FileUseCase
from app.user.application.dto import DownloadFileRequestDTO

file_router = APIRouter()


@file_router.post(
    "/upload",
)
@inject
async def upload_file(
    request: UploadFile = File(...),
    usecase: FileUseCase = Depends(Provide[Container.file_service])
):
    await usecase.upload_file(file=request)


@file_router.get(
    "/download/{file_id}",
)
@inject
async def download_file(
    file_id: int,
    request: DownloadFileRequestDTO,
    usecase: FileUseCase = Depends(Provide[Container.file_service])
):
    return await usecase.download_file(file_id=file_id, filename=request.filename if request.filename else None)
