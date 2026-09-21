from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(examples=["ana@example.com"])
    password: str = Field(min_length=1, examples=["clave123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
