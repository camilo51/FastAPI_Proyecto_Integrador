from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("rol IN ('cliente', 'admin')", name="check_user_role"),)

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default="cliente")

    pedidos = relationship("Order", back_populates="usuario")
