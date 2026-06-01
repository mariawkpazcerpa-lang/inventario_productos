from flask import Flask, jsonify, request
import inventario  # importa tu archivo principal

app = Flask(__name__)

@app.route("/")
def home():
    return "Inventario en línea funcionando"

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
