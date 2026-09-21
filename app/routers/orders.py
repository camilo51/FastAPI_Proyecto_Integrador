from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Pedidos"])


def get_order_or_404(order_id: int, db: Session) -> Order:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, summary="Crear pedido")
def create_order(order_data: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Crea el pedido, calcula el total y descuenta el stock automáticamente."""
    total = Decimal("0")
    products_to_buy: list[tuple[Product, int]] = []
    quantities_requested: dict[int, int] = {}

    # Primero se valida todo el pedido. Aún no se modifica el stock.
    for item_data in order_data.productos:
        product = db.query(Product).filter(Product.id == item_data.producto_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        requested = quantities_requested.get(product.id, 0) + item_data.cantidad
        if product.stock < requested:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto {product.nombre}")
        quantities_requested[product.id] = requested
        products_to_buy.append((product, item_data.cantidad))

    # Al ser válido, se calcula el total, se conserva el precio actual y se descuenta el stock.
    items_to_create: list[tuple[Product, int, Decimal]] = []
    for product, quantity in products_to_buy:
        price_at_purchase = product.precio
        product.stock -= quantity
        total += price_at_purchase * quantity
        items_to_create.append((product, quantity, price_at_purchase))

    order = Order(usuario_id=current_user.id, estado="pendiente", total=total)
    db.add(order)
    db.flush()

    for product, quantity, price_at_purchase in items_to_create:
        db.add(OrderItem(
            pedido_id=order.id,
            producto_id=product.id,
            cantidad=quantity,
            precio_unitario=price_at_purchase,
        ))

    db.commit()
    return get_order_or_404(order.id, db)


@router.get("/my-orders", response_model=list[OrderResponse], summary="Consultar mis pedidos")
def my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.usuario_id == current_user.id)
        .order_by(Order.id.desc())
        .all()
    )


@router.get("", response_model=list[OrderResponse], summary="Listar todos los pedidos")
def list_orders(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Order).options(joinedload(Order.items)).order_by(Order.id.desc()).all()


@router.get("/{order_id}", response_model=OrderResponse, summary="Consultar un pedido")
def get_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_or_404(order_id, db)
    if current_user.rol != "admin" and order.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse, summary="Cambiar estado de pedido")
def update_order_status(order_id: int, status_data: OrderStatusUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    order = get_order_or_404(order_id, db)
    order.estado = status_data.estado
    db.commit()
    return get_order_or_404(order_id, db)
