from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from app.auth.adapter.input.api.v1.request import RefreshTokenRequest
from app.auth.adapter.input.api.v1.response import RefreshTokenResponse
from app.auth.domain.usecase.jwt import JwtUseCase
from app.container import Container

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: JwtUseCase = Depends(Provide[Container.jwt_service]),
):
    token = await usecase.create_refresh_token(
        token=request.accessToken, refresh_token=request.refreshToken
    )
    return {"accessToken": token.accessToken}
