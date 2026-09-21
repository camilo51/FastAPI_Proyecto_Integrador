from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado')",
            name="check_order_status",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    estado = Column(String(20), nullable=False, default="pendiente")
    total = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)

    usuario = relationship("User", back_populates="pedidos")
    items = relationship("OrderItem", back_populates="pedido", cascade="all, delete-orphan")
