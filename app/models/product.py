from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("precio > 0", name="check_product_price"),
        CheckConstraint("stock >= 0", name="check_product_stock"),
    )

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    categoria = relationship("Category", back_populates="productos")
    items_pedido = relationship("OrderItem", back_populates="producto")
