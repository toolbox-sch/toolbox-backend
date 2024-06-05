from pydantic import BaseModel, Field


class RefreshTokenResponseDTO(BaseModel):
    accessToken: str = Field(..., description="Token")
