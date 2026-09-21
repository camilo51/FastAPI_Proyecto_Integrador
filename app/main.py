from fastapi import FastAPI

from app.routers import auth, categories, orders, products

app = FastAPI(
    title="API de Inventario y Pedidos",
    description="Proyecto académico para gestionar usuarios, catálogo, stock y pedidos.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", tags=["Inicio"])
def home():
    return {"message": "API de Inventario y Pedidos funcionando"}
