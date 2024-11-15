from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    cnx = mysql.connector.connect(user='root', password='obligatorio', host='127.0.0.1', database='obligatorio')
    return cnx

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

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('alumnos'))
        else:
            return render_template('login.html', error="email o contraseña incorrectos.")
    return render_template('login.html')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')  # Si no existe 'nombre', asignar un valor vacío
        apellido = request.form.get('apellido', '')  # Lo mismo para 'apellido'
        actividad = request.form.get('actividad', '')  # Y para 'actividad'
        alquila = request.form.get('alquila', '')  # Y para 'alquila'

        # Conectar a la base de datos y hacer la consulta
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)  # Usar dictionary=True para que el resultado sea más fácil de manejar

        # Construcción de la consulta base
        query = "SELECT ciAlumno, nombre, apellido, fecha_nacimiento, idActividad, alquila FROM alumnos WHERE 1=1"

        # Lista para los parámetros de la consulta
        params = []

        # Agregar condiciones dinámicas si los campos no están vacíos
        if nombre:
            query += " AND nombre LIKE %s"
            params.append('%' + nombre + '%')

        if apellido:
            query += " AND apellido LIKE %s"
            params.append('%' + apellido + '%')

        if actividad:
            query += " AND id_actividad LIKE %s"
            params.append('%' + actividad + '%')

        if alquila:
            query += " AND alquila LIKE %s"
            params.append('%' + alquila + '%')

        # Ejecutar la consulta con los parámetros
        cursor.execute(query, params)
        alumnos_result = cursor.fetchall()  # Obtener todos los resultados
        cursor.close()
        cnx.close()

        return render_template('pestañas.html', alumnos=alumnos_result)
    return render_template('pestañas.html')

@app.route('/equipamiento', methods=['GET', 'POST'])
def equipamiento():
    if request.method == 'POST':
        # Obtener los valores del formulario
        id = request.form.get('id', '').strip()
        actividad = request.form.get('actividad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        costo = request.form.get('costo', '').strip()

        # Conectar a la base de datos
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        # Consulta base
        query = "SELECT idEquipamiento, idActividad, descripcion, costo FROM equipamiento WHERE 1=1"

        # Lista para los parámetros de la consulta
        params = []

        # Agregar condiciones dinámicas si los campos no están vacíos
        if id:
            query += " AND idEquipamiento LIKE %s"
            params.append('%' + id + '%')

        if actividad:
            query += " AND idActividad LIKE %s"
            params.append('%' + actividad + '%')

        if descripcion:
            query += " AND descripcion LIKE %s"
            params.append('%' + descripcion + '%')

        if costo:
            query += " AND costo LIKE %s"
            params.append('%' + costo + '%')

        # Ejecutar la consulta con los parámetros
        cursor.execute(query, params)
        equipamiento_result = cursor.fetchall()  # Obtener todos los resultados
        cursor.close()
        cnx.close()

        # Pasar los resultados a la plantilla
        return render_template('pestañas.html', equipamientos=equipamiento_result)

    # Si la solicitud es GET, simplemente renderizamos la página vacía
    return render_template('pestañas.html')




if __name__ == '__main__':
    app.run(debug=True)
