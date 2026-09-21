import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.request import request_context_middleware
from app.routers import auth, categories, orders, products

load_dotenv()


def get_cors_origins() -> list[str]:
    """Obtiene los orígenes permitidos desde CORS_ALLOW_ORIGINS."""
    configured_origins = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

app = FastAPI(
    title="API de Inventario y Pedidos",
    description="Proyecto académico para gestionar usuarios, catálogo, stock y pedidos.",
    version="1.0.0",
)

# CORS debe registrarse antes de las rutas para atender también solicitudes OPTIONS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-Process-Time-Ms"],
)
app.middleware("http")(request_context_middleware)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", tags=["Inicio"])
def home():
    return {"message": "API de Inventario y Pedidos funcionando"}
