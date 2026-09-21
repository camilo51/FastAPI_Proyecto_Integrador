# Sistema de Gestión de Inventario y Pedidos

API académica construida con FastAPI para administrar usuarios, categorías, productos, stock y pedidos. Hay dos roles: cliente y admin.

## Requisitos e instalación

Se recomienda Python 3.10 o superior. Desde la carpeta del proyecto, cree y active un entorno virtual:

    python -m venv venv
    .\venv\Scripts\Activate.ps1

En Linux/macOS el comando de activación es source venv/bin/activate.

Instale las dependencias:

    pip install -r requirements.txt

El archivo .env ya contiene la configuración de desarrollo. Puede cambiar la clave JWT antes de usar el proyecto fuera de un entorno local:

    DATABASE_URL=sqlite:///./ecommerce.db
    SECRET_KEY=una_clave_para_desarrollo
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

## Base de datos y migraciones

Las tablas se crean mediante Alembic, no automáticamente al iniciar FastAPI. La migración inicial ya está incluida. Ejecute:

    alembic upgrade head

Cuando cambie los modelos en el futuro, puede generar una nueva migración con:

    alembic revision --autogenerate -m "descripcion del cambio"
    alembic upgrade head

## Crear el administrador

Después de aplicar las migraciones, ejecute el script y escriba los datos solicitados:

    python create_admin.py

El registro público (POST /auth/register) crea exclusivamente usuarios con rol cliente.

## Iniciar la API

    uvicorn app.main:app --reload

Abra Swagger en http://127.0.0.1:8000/docs.

## Flujo de prueba en Swagger

1. Cree un cliente con POST /auth/register o inicie sesión con el administrador creado por script.
2. Use POST /auth/login; copie el valor de access_token.
3. Pulse Authorize arriba en Swagger, pegue el token sin escribir Bearer y autorice.
4. Con un administrador, cree una categoría y un producto, indicando un stock mayor que cero.
5. Inicie sesión como cliente, autorícese con su token y cree un pedido en POST /orders.
6. Consulte el resultado en GET /orders/my-orders. El stock se reduce al crear el pedido.

## Estructura

- app/main.py: crea FastAPI e incluye las rutas.
- app/database.py: conexión síncrona de SQLAlchemy y sesión por solicitud.
- app/models/: tablas y relaciones de SQLAlchemy.
- app/schemas/: validación de entradas y respuestas de Pydantic.
- app/routers/: endpoints organizados por tema.
- app/dependencies/: autenticación y comprobación de administrador.
- app/middlewares/: trazabilidad HTTP; asigna `X-Request-ID` y `X-Process-Time-Ms`.
- app/utils/security.py: hash de contraseñas y JWT.
- alembic/: configuración e historial de migraciones.
- create_admin.py: script interactivo para crear el administrador inicial.
