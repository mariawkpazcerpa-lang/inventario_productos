# Sistema de Inventario de Productos

Este proyecto en **Python** simula un inventario estilo supermercado.  
Permite **agregar, eliminar, modificar y listar productos** mediante una interfaz de consola, conectado a una base de datos **SQLite** y usando **Colorama** para resaltar textos importantes.

---

## 🛠 Tecnologías utilizadas
- Python 3.x
- SQLite (base de datos)
- Colorama (colores en consola)
- Librerías estándar de Python: `sqlite3`, `os`, `sys`

---

## 💻 Cómo ejecutar el proyecto

1. Cloná el repositorio:
```bash
git clone https://github.com/tuusuario/inventario-productos.git
Entrá a la carpeta del proyecto:

bash
Copiar código
cd inventario-productos
Instalá las dependencias:

bash
Copiar código
pip install -r requirements.txt
Ejecutá el programa:

bash
Copiar código
python main.py
Al ejecutarlo por primera vez, la base de datos SQLite se crea automáticamente.

⚙️ Funcionalidades
Agregar productos: Nombre, precio, cantidad

Modificar productos existentes: cambiar nombre, precio o cantidad

Eliminar productos del inventario

Listar productos para ver el inventario completo

Resaltar información clave en la consola usando Colorama

🔹 Ejemplo de uso
text
Copiar código
*~~*INVENTARIO*~~*
*~~Menú Principal~~*
1 ~ Registrar un nuevo producto.
2 ~ Visualizar lista del inventario.
3 ~ Buscar un producto.
4 ~ Actualizar un producto.
5 ~ Eliminar un producto.
6 ~ Reporte de productos con bajo stock.
7 ~ Salir.
Ingresa la opcion deseada: 1

~~Registrar producto nuevo~~
Ingresa el nombre del producto: Leche Entera Vaquita
Ingresa la descripción del producto: 1Lt de Leche Entera Vaquita en Sachet. Vence el 30/9/2025
Ingresa el precio del producto (Por favor use punto, no coma): 1250 
Ingresa la cantidad de unidades del producto: 100
Ingresa la categoria del producto: Lacteos
Producto Leche entera vaquita registrado correctamente

Ingresa la opcion deseada: 2
Lista de productos:
ID: 1 | Nombre: Leche entera vaquita | Descripción: 1lt de leche entera vaquita en sachet. vence el 30/9/2025 | Cantidad: 100 | Precio: 1250.0 | Categoría: Lacteos

📷 Vista previa
Un vistazo general de las funciones uno y dos del menú
(Captura de pantalla 2025-09-19 190607.png)

🔗 Repositorio de código
Código completo: https://github.com/mariawkpazcerpa-lang/inventario_productos

📬 Contacto
Email: mariawkpazcerpa@gmail.com

LinkedIn: María de la Paz Cerpa
