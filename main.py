from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

inventario = [
    {"id": 1, "nombre": "Coca-Cola", "precio": 20, "cantidad": 25},
    {"id": 2, "nombre": "Papas", "precio": 15, "cantidad": 40},
    {"id": 3, "nombre": "Café", "precio": 18, "cantidad": 15}
]


@app.get("/")
def home():
    return {"Message": "Hola bienvenido"}


@app.get("/productos")
def getProductos():
    return inventario


@app.post("/productos")
def addProducto(producto: dict):

    nuevo_id = max(
        [p["id"] for p in inventario],
        default=0
    ) + 1

    nuevo_producto = {
        "id": nuevo_id,
        "nombre": producto["nombre"],
        "precio": float(producto["precio"]),
        "cantidad": int(producto["cantidad"])
    }

    inventario.append(nuevo_producto)

    return {
        "Message": "Producto agregado con éxito",
        "producto": nuevo_producto
    }


@app.put("/productos/{producto_id}")
def updateProducto(producto_id: int, producto_actualizado: dict):

    for i, producto in enumerate(inventario):

        if producto["id"] == producto_id:

            inventario[i] = {
                **producto,
                **producto_actualizado
            }

            return {
                "Message": "El producto fue actualizado",
                "producto": inventario[i]
            }

    return {
        "Message": "El producto no fue encontrado"
    }


@app.delete("/productos/{producto_id}")
def deleteProducto(producto_id: int):

    for i, producto in enumerate(inventario):

        if producto["id"] == producto_id:

            producto_eliminado = inventario.pop(i)

            return {
                "Message": "Producto eliminado con éxito",
                "producto": producto_eliminado
            }

    return {
        "Message": "El producto no fue encontrado"
    }
