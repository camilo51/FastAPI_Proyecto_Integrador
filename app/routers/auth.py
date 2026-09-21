from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRegister, UserResponse
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar cliente")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Crea un usuario público. Siempre se asigna el rol cliente."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user = User(
        nombre=user_data.nombre,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        rol="cliente",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Devuelve un JWT para usar en el botón Authorize de Swagger."""
    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": str(user.id), "rol": user.rol})
    return {"access_token": token, "token_type": "bearer"}
