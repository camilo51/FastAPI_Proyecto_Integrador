from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150, examples=["Camiseta"])
    descripcion: str | None = Field(default=None, max_length=500)
    precio: Decimal = Field(gt=0, examples=[39900])
    stock: int = Field(ge=0, examples=[20])
    categoria_id: int = Field(gt=0, examples=[1])

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip()


class ProductUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    categoria_id: int | None = Field(default=None, gt=0)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip() if value is not None else value


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    precio: Decimal
    stock: int
    categoria_id: int
