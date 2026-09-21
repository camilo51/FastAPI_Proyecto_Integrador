from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

OrderStatus = Literal["pendiente", "procesando", "enviado", "entregado", "cancelado"]


class OrderProductCreate(BaseModel):
    producto_id: int = Field(gt=0, examples=[1])
    cantidad: int = Field(gt=0, examples=[2])


class OrderCreate(BaseModel):
    productos: list[OrderProductCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    estado: OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    estado: OrderStatus
    total: Decimal
    fecha: datetime
    items: list[OrderItemResponse]
