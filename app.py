from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

# Creación de base de datos y tabla
def init_database():
    # Se crea la base de datos en caso de que no exista
    conn = sqlite3.connect("almacen.db")
    
    cursor =  conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto(
            id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio FLOAT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/producto")
def producto():
    conn = sqlite3.connect("almacen.db")
    # Permite manejar los registros como diccionarios
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    producto = cursor.fetchall()
    return render_template("producto/index.html",producto = producto)

@app.route("/producto/create")
def create():
    return render_template('producto/create.html')

@app.route("/producto/create/save",methods=['POST'])
def producto_save():
    descripcion =  request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO producto (descripcion,cantidad,precio) VALUES (?,?,?)", (descripcion, cantidad,precio))
    
    conn.commit()
    conn.close()
    return redirect('/producto')

# Editar producto
@app.route("/producto/edit/<int:id>")
def producto_edit(id):
    conn =  sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor =  conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("producto/edit.html",producto = producto)

@app.route("/producto/update",methods=['POST'])
def producto_update():
    id = request.form['id']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    conn  = sqlite3.connect("almacen.db")
    cursor =  conn.cursor()
    
    cursor.execute("UPDATE producto SET descripcion=?,cantidad=?,precio=? WHERE id=?", (descripcion,cantidad,precio,id))
    conn.commit()
    conn.close()
    return redirect("/producto")

# Eliminar registro
@app.route("/producto/delete/<int:id>")
def producto_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/producto')
    
if __name__ == "__main__":
    app.run(debug=True)