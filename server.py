from flask import Flask, jsonify
import inventario  # tu archivo original

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor Flask funcionando. Bienvenida al inventario."

@app.route("/productos")
def productos():
    # llamar directamente a la función de tu CRUD
    conexion = inventario.sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()
    conexion.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)