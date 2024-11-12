from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# Función para obtener la conexión a la base de datos
def get_db_connection():
    cnx = mysql.connector.connect(user='root', password='obligatorio', host='127.0.0.1', database='obligatorio')
    return cnx

# Ejemplo de uso: Realizar una consulta simple
@app.route('/ver_actividades')
def ver_actividades():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM actividades"
    cursor.execute(query)
    actividades = cursor.fetchall()  # Obtiene todos los resultados de la consulta
    cnx.close()

    # Pasar los resultados a la plantilla para mostrarlos
    return render_template('ver_actividades.html', actividades=actividades)



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']

        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = """
        INSERT INTO login (nombre, apellido, email, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, apellido, email, password))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET','POST'])
def do_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "SELECT * FROM login WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        email = cursor.fetchone()
        cursor.close()
        cnx.close()

        if email:
            return redirect(url_for('tabs'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")
    return render_template('login.html')

@app.route('/pestañas')
def tabs():
    return render_template('pestañas.html')

@app.route('/alumno', methods=['GET', 'POST'])
def nuevo_alumno():
    return render_template('nuevoAlumno.html')

@app.route('/instructor', methods=['GET', 'POST'])
def nuevo_instructor():
    return render_template('nuevoInstructor.html')

@app.route('/clase', methods=['GET', 'POST'])
def nueva_clase():
    return render_template('nuevaClase.html')

@app.route('/equipamiento', methods=['GET', 'POST'])
def nuevo_equipamiento():
    return render_template('nuevoEquipamiento.html')

@app.route('/cambiar_contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        nueva_contrasena = request.form['nueva-contrasena']
        confirmar_contrasena = request.form['confirmarContrasena']

        if nueva_contrasena == confirmar_contrasena:
            cnx = get_db_connection()
            cursor = cnx.cursor()
            query = "UPDATE login SET password = %s WHERE email = %s"
            cursor.execute(query, (nueva_contrasena, email))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('login', mensaje='Contraseña cambiada exitosamente'))
        else:
            return redirect(url_for('cambiar_contrasena', mensaje='Las contraseñas no coinciden'))

    mensaje = request.args.get('mensaje')
    return render_template('cambiarContraseña.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)