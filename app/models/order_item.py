from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (CheckConstraint("cantidad > 0", name="check_order_item_quantity"),)

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Order", back_populates="items")
    producto = relationship("Product", back_populates="items_pedido")
