from flask import Flask, jsonify, request
import inventario  # importa tu archivo principal

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1 style='color:blue;'>*~~* INVENTARIO *~~*</h1>
    <h2>Menú Principal</h2>
    <ul>
        <li><a href='/registrar'>1 ~ Registrar un nuevo producto</a></li>
        <li><a href='/productos'>2 ~ Visualizar lista del inventario</a></li>
        <li><a href='/buscar/1'>3 ~ Buscar un producto por ID</a></li>
        <li><a href='/buscar/nombre/ProductoX'>3b ~ Buscar un producto por nombre</a></li>
        <li><a href='/buscar/categoria/Bebidas'>3c ~ Buscar productos por categoría</a></li>
        <li><a href='/actualizar/1'>4 ~ Actualizar un producto</a></li>
        <li><a href='/eliminar/1'>5 ~ Eliminar un producto</a></li>
        <li><a href='/reporte/20'>6 ~ Reporte de productos con bajo stock</a></li>
        <li><a href='/salir'>7 ~ Salir (cerrar sesión)</a></li>
    </ul>
    <p style='color:gray;'>Seleccioná una opción del menú para interactuar con el inventario.</p>
    """

# --- LISTAR PRODUCTOS ---
@app.route("/productos")
def productos():
    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()
    conexion.close()
    return jsonify(data)

# --- REGISTRAR PRODUCTO ---
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    precio = request.form.get("precio")
    cantidad = request.form.get("cantidad")
    categoria = request.form.get("categoria")

    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria)
        VALUES (?,?,?,?,?)
    ''', (nombre, descripcion, float(precio), int(cantidad), categoria))
    conexion.commit()
    conexion.close()

    return f"Producto {nombre} registrado correctamente"

# --- BUSCAR PRODUCTO POR ID ---
@app.route("/buscar/<int:id_producto>")
def buscar(id_producto):
    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    conexion.close()
    if producto:
        return jsonify(producto)
    else:
        return "Producto no encontrado", 404

# --- ACTUALIZAR PRODUCTO ---
@app.route("/actualizar/<int:id_producto>", methods=["PUT"])
def actualizar(id_producto):
    campo = request.form.get("campo")
    valor = request.form.get("valor")

    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (valor, id_producto))
    conexion.commit()
    conexion.close()

    return f"Producto {id_producto} actualizado correctamente"

# --- ELIMINAR PRODUCTO ---
@app.route("/eliminar/<int:id_producto>", methods=["DELETE"])
def eliminar(id_producto):
    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()
    return f"Producto con ID {id_producto} eliminado"

# --- REPORTE DE STOCK ---
@app.route("/reporte/<int:limite>")
def reporte(limite):
    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    resultado = cursor.fetchall()
    conexion.close()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run()
