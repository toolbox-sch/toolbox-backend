from pydantic import BaseModel, Field


class RefreshTokenResponse(BaseModel):
    accessToken: str = Field(..., description="Access Token")
