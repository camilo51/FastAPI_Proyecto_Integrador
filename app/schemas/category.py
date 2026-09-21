from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, examples=["Ropa"])
    descripcion: str | None = Field(default=None, max_length=255, examples=["Prendas de vestir"])

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip()


class CategoryUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip() if value is not None else value


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
