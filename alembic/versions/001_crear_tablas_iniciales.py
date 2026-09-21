"""crear tablas iniciales

Revision ID: 001_crear_tablas_iniciales
Revises:
Create Date: 2026-09-20
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_crear_tablas_iniciales"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("rol", sa.String(length=20), nullable=False),
        sa.CheckConstraint("rol IN ('cliente', 'admin')", name="check_user_role"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.String(length=500), nullable=True),
        sa.Column("precio", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.CheckConstraint("precio > 0", name="check_product_price"),
        sa.CheckConstraint("stock >= 0", name="check_product_stock"),
        sa.ForeignKeyConstraint(["categoria_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False),
        sa.Column("total", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.CheckConstraint("estado IN ('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado')", name="check_order_status"),
        sa.ForeignKeyConstraint(["usuario_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.CheckConstraint("cantidad > 0", name="check_order_item_quantity"),
        sa.ForeignKeyConstraint(["pedido_id"], ["orders.id"]),
        sa.ForeignKeyConstraint(["producto_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_items_id"), "order_items", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_order_items_id"), table_name="order_items")
    op.drop_table("order_items")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
