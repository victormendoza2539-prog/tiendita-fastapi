"""
Titulo: Proyecto tiendita
Autor: Victor H. Mendoza
Fecha de creación: 06-10-2026
Descripción: Configuración de una API para gestionar un inventario de productos en una 
tienda utilizando FastAPI. La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) 
sobre los productos del inventario.
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio
import time


app = FastAPI(
    title="API Proyecto Tiendita",
    description="API para gestionar el inventario de productos",
    version="1.0"
)


# ==========================================
# MIDDLEWARE: MAXIMO 5 PETICIONES POR SEGUNDO
# ==========================================

MAX_PETICIONES = 5
DURACION_VENTANA = 1.0

inicio_ventana = time.monotonic()
contador_peticiones = 0
candado = asyncio.Lock()


@app.middleware("http")
async def limitar_peticiones(request, call_next):
    global inicio_ventana, contador_peticiones

    # Obtenemos el tiempo actual
    ahora = time.monotonic()

    # Protegemos el contador ante solicitudes simultaneas
    async with candado:

        # Reiniciamos el contador cada segundo
        if ahora - inicio_ventana >= DURACION_VENTANA:
            inicio_ventana = ahora
            contador_peticiones = 0

        # Si ya se alcanzo el limite, rechazamos la solicitud
        if contador_peticiones >= MAX_PETICIONES:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Demasiadas peticiones",
                    "mensaje": "Maximo 5 peticiones por segundo"
                }
            )

        # Registramos la peticion permitida
        contador_peticiones += 1

    # Continuamos con la ruta solicitada
    respuesta = await call_next(request)

    return respuesta


# ==========================================
# CONFIGURACION CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# MODELO DE PRODUCTO
# ==========================================

class Producto(BaseModel):
    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del producto"
    )
    precio: float = Field(
        ...,
        gt=0,
        description="Precio del producto"
    )
    cantidad: int = Field(
        ...,
        ge=0,
        description="Stock del producto"
    )


# ==========================================
# INVENTARIO INICIAL
# ==========================================

inventario = [
    {"id": 1, "nombre": "Coca-Cola", "precio": 20, "cantidad": 25},
    {"id": 2, "nombre": "Papas", "precio": 15, "cantidad": 40},
    {"id": 3, "nombre": "Cafe", "precio": 18, "cantidad": 15}
]


# ==========================================
# RUTAS DE LA API
# ==========================================

@app.get("/")
async def home():
    return {"message": "Hola, bienvenido a la tiendita"}


@app.get("/procesar")
async def procesar_pedido():
    # Simula una consulta a la base de datos de 2 segundos
    await asyncio.sleep(2)
    return {"message": "Pedido procesado con exito"}


@app.get("/productos")
async def get_productos():
    return inventario


@app.post("/productos")
async def add_producto(producto: Producto):

    nuevo_id = max(
        [p["id"] for p in inventario],
        default=0
    ) + 1

    nuevo_producto = {
        "id": nuevo_id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "cantidad": producto.cantidad
    }

    inventario.append(nuevo_producto)

    return {
        "message": "Producto agregado con exito",
        "producto": nuevo_producto
    }
    inventario.append(nuevo_producto)

    return {
        "message": "Producto agregado con exito",
        "producto": nuevo_producto
    }


@app.put("/productos/{producto_id}")
async def update_producto(
    producto_id: int,
    producto_actualizado: dict
):
    for i, producto in enumerate(inventario):
        if producto["id"] == producto_id:

            inventario[i] = {
                **producto,
                **producto_actualizado
            }

            return {
                "message": "Producto actualizado",
                "producto": inventario[i]
            }

    return {"message": "Producto no encontrado"}


@app.delete("/productos/{producto_id}")
async def delete_producto(producto_id: int):

    for i, producto in enumerate(inventario):
        if producto["id"] == producto_id:

            producto_eliminado = inventario.pop(i)

            return {
                "message": "Producto eliminado con exito",
                "producto": producto_eliminado
            }

    return {"message": "Producto no encontrado"}