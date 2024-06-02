from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    accessToken: str = Field(..., description="Token")
    refreshToken: str = Field(..., description="Refresh token")
