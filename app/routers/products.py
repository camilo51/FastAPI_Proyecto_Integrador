from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Productos"])


def get_product_or_404(product_id: int, db: Session) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


def validate_category(category_id: int, db: Session) -> None:
    if db.query(Category).filter(Category.id == category_id).first() is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")


@router.get("", response_model=list[ProductResponse], summary="Listar productos")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()


@router.get("/{product_id}", response_model=ProductResponse, summary="Consultar un producto")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(product_id, db)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Crear producto")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    validate_category(product_data.categoria_id, db)
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse, summary="Actualizar producto")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    product = get_product_or_404(product_id, db)
    changes = product_data.model_dump(exclude_unset=True)
    if "categoria_id" in changes:
        validate_category(changes["categoria_id"], db)
    for field, value in changes.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK, summary="Eliminar producto")
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    product = get_product_or_404(product_id, db)
    db.delete(product)
    db.commit()
    return {"message": "Producto eliminado correctamente"}
