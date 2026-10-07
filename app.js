const API_URL = "http://localhost:8000/productos";
// Selección de Elementos del DOM
const formProducto = document.getElementById("formProducto");
const tablaProductos = document.getElementById("tablaProductos");
const totalProductos = document.getElementById("totalProductos");

// 1. Función para Cargar Productos (GET)
async function cargarProductos() {
    try {
        const respuesta = await fetch(API_URL);
        const productos = await respuesta.json();

        tablaProductos.innerHTML = "";
        totalProductos.textContent = `${productos.length} productos`;

        if (productos.length === 0) {
            tablaProductos.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted py-4">
                        No hay productos registrados en la tiendita.
                    </td>
                </tr>`;
            return;
        }

        

        productos.forEach(p => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td class="fw-bold text-secondary">#${p.id}</td>
                <td>${p.nombre}</td>
                <td class="text-success fw-bold">$${p.precio.toFixed(2)}</td>
                <td>
                    <span class="badge ${p.cantidad < 10 ? 'bg-danger' : 'bg-success'}">
                        ${p.cantidad} unidades
                    </span>
                </td>
                <td class="text-end">
                    <button class="btn btn-outline-danger btn-sm" onclick="eliminarProducto(${p.id})">
                        <i class="bi bi-trash"></i> Eliminar
                    </button>
                </td>
            `;
            tablaProductos.appendChild(fila);
        });

    } catch (error) {
        console.error("Error al cargar productos:", error);
    }
}


// Cargar catálogo al abrir la página
document.addEventListener("DOMContentLoaded", cargarProductos);

// 2. Función para Agregar Producto (POST)
formProducto.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nuevoProducto = {
        nombre: document.getElementById("nombre").value,
        precio: parseFloat(document.getElementById("precio").value),
        cantidad: parseInt(document.getElementById("cantidad").value)
    };

    try {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(nuevoProducto)
        });

        if (respuesta.ok) {
            formProducto.reset();
            cargarProductos(); // Refresca la tabla
        }
    } catch (error) {
        console.error("Error al guardar producto:", error);
    }
});

// 3. Función para Eliminar Producto (DELETE)
async function eliminarProducto(id) {
    if (!confirm("¿Deseas eliminar este producto?")) return;

    try {
        const respuesta = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (respuesta.ok) {
            cargarProductos(); // Refresca la tabla
        }
    } catch (error) {
        console.error("Error al eliminar producto:", error);
    }
}