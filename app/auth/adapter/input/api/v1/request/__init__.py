from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    accessToken: str = Field(..., description="Token")
    refreshToken: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
    accessToken: str = Field(..., description="Token")
