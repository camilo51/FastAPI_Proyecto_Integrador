from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categorías"])


def get_category_or_404(category_id: int, db: Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.get("", response_model=list[CategoryResponse], summary="Listar categorías")
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()


@router.get("/{category_id}", response_model=CategoryResponse, summary="Consultar una categoría")
def get_category(category_id: int, db: Session = Depends(get_db)):
    return get_category_or_404(category_id, db)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Crear categoría")
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    if db.query(Category).filter(Category.nombre == category_data.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse, summary="Actualizar categoría")
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    category = get_category_or_404(category_id, db)
    changes = category_data.model_dump(exclude_unset=True)
    if "nombre" in changes:
        duplicate = db.query(Category).filter(Category.nombre == changes["nombre"], Category.id != category_id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    for field, value in changes.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK, summary="Eliminar categoría")
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    category = get_category_or_404(category_id, db)
    if db.query(Product).filter(Product.categoria_id == category_id).first():
        raise HTTPException(status_code=400, detail="No se puede eliminar la categoría porque tiene productos asociados")
    db.delete(category)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}
