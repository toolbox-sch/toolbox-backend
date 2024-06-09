from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, File, Request

from app.container import Container
from app.user.application.dto import PdfSplitterRequestDTO, PdfEncryptRequestDTO, ConvertImageRequestDTO
from app.user.domain.usecase.tool import ToolUseCase
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated

tool_router = APIRouter()


@tool_router.post(
    "/pdf/merge",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def merge_pdf(
    request: Request,
    file: List[UploadFile] = File(...),
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filename = await usecase.merge_pdf(files=file, user_id=request.user.id)
    return {"filename": filename}


@tool_router.post(
    "/pdf/split",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def split_pdf(
    request: Request,
    dto: PdfSplitterRequestDTO,
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filename = await usecase.split_pdf(
        file=dto.file,
        start=dto.start,
        end=dto.end,
        user_id=request.user.id
    )

    return {"filename": filename}


@tool_router.post(
    "/pdf/encrypt",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def encrypt_pdf(
    request: Request,
    dto: PdfEncryptRequestDTO,
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filename = await usecase.encrypt_pdf(file=dto.file, key=dto.key, user_id=request.user.id)
    return {"filename": filename}


@tool_router.post(
    "/pdf/extract",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def extract_pdf_text(
    request: Request,
    file: UploadFile = File(...),
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filename = await usecase.extract_pdf_text(file=file, user_id=request.user.id)
    return {"filename": filename}


@tool_router.post(
    "/pdf/convert_to_png",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def pdf_to_png(
    request: Request,
    file: UploadFile = File(...),
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filenames = await usecase.pdf_to_png(file=file, user_id=request.user.id)
    return {"filenames": filenames}


@tool_router.post(
    "/image/convert",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def convert_image(
    request: Request,
    dto: ConvertImageRequestDTO,
    usecase: ToolUseCase = Depends(Provide[Container.tool_service])
):
    filename = await usecase.convert_image(file=dto.file, target=dto.target, user_id=request.user.id)
    return {"filename": filename}
