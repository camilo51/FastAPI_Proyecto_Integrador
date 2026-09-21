from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, examples=["Ana Pérez"])
    email: EmailStr = Field(examples=["ana@example.com"])
    password: str = Field(min_length=6, max_length=100, examples=["clave123"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    rol: Literal["cliente", "admin"]
