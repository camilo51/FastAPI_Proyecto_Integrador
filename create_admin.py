"""Crea el primer administrador desde la terminal."""
from getpass import getpass

from email_validator import EmailNotValidError, validate_email

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password


def main():
    db = SessionLocal()
    try:
        nombre = input("Nombre del administrador: ").strip()
        email = input("Email del administrador: ").strip().lower()
        password = getpass("Contraseña (mínimo 6 caracteres): ")

        if not nombre or len(password) < 6:
            print("El nombre y una contraseña de al menos 6 caracteres son obligatorios.")
            return
        try:
            email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError:
            print("El email no es válido.")
            return
        if db.query(User).filter(User.email == email).first():
            print("Ya existe un usuario con ese email.")
            return

        admin = User(nombre=nombre, email=email, hashed_password=hash_password(password), rol="admin")
        db.add(admin)
        db.commit()
        print("Administrador creado correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
