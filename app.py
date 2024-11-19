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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Asegúrate de tener este archivo HTML

@app.route('/alumnos')
def alumnos_page():
    return render_template('alumnos.html')

@app.route('/nuevoAlumno')
def nuevo_alumno():
    return render_template('nuevoAlumno.html')

@app.route('/instructor')
def nuevo_instructor():
    return render_template('nuevoInstructor.html')
@app.route('/nuevaClase')
def nueva_clase():
    return render_template('nuevaClase.html')
@app.route('/nuevoEquipamiento')
def nuevo_equipamiento():
    return render_template('nuevoEquipamiento.html')
@app.route('/equipamiento')
def equipamiento_page():
    return render_template('equipamiento.html')

@app.route('/clase')
def clase_page():
    return render_template('clase.html')

@app.route('/instructores')
def instructores_page():
    return render_template('instructores.html')

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
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="email o contraseña incorrectos.")
    return render_template('login.html')

@app.route('/buscar_instructores', methods=['POST'])
def buscar_instructores():
    # Obtener los valores del formulario
    nombre = request.form.get('nombreInstructor', '').strip()
    apellido = request.form.get('apellidoInstructor', '').strip()
    ci = request.form.get('ci', '').strip()

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    # Consulta base
    query = "SELECT ciInstructor, nombre, apellido"
    query += " FROM instructores"
    query += " WHERE 1=1"
    params = []

    # Agregar condiciones dinámicas si los campos no están vacíos
    if ci:
        query += " AND ciInstructor LIKE %s"
        params.append('%' + ci + '%')

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')

    if apellido:
        query += " AND apellido LIKE %s"
        params.append('%' + apellido + '%')

    # Ejecutar la consulta
    cursor.execute(query, params)
    instructores_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Pasar los resultados a la plantilla
    return render_template('instructores.html', instructores=instructores_result)

@app.route('/buscar_alumnos', methods=['POST'])
def buscar_alumnos():
    # Obtener los valores del formulario
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    alquila = request.form.get('alquila', '').strip()

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    # Consulta base
    query = "SELECT ciAlumno, nombre, apellido, fecha_nacimiento, descripcion, alquila"
    query += " FROM alumnos"
    query += " INNER JOIN actividades ON actividades.idActividad = alumnos.idActividad"
    query += " WHERE 1=1"
    params = []

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')

    if apellido:
        query += " AND apellido LIKE %s"
        params.append('%' + apellido + '%')

    if descripcion:
        query += " AND descripcion LIKE %s"
        params.append('%' + descripcion + '%')

    if alquila:
        query += " AND alquila LIKE %s"
        params.append('%' + alquila + '%')

    # Ejecutar la consulta
    cursor.execute(query, params)
    alumnos_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Pasar los resultados a la plantilla
    return render_template('alumnos.html', alumnos=alumnos_result)

@app.route('/buscar_equipamiento', methods=['POST'])
def buscar_equipamiento():
    # Obtener los valores del formulario
    id = request.form.get('id', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    actividad = request.form.get('actividad', '').strip()
    costo = request.form.get('costo', '').strip()

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    # Consulta base
    query = "SELECT idEquipamiento, descripcion, costo, idActividad"
    query += " FROM equipamiento"
    query += " WHERE 1=1"
    params = []

    # Agregar condiciones dinámicas si los campos no están vacíos
    if id:
        query += " AND idEquipamiento LIKE %s"
        params.append('%' + id + '%')

    if descripcion:
        query += " AND descripcion LIKE %s"
        params.append('%' + descripcion + '%')

    if actividad:
        query += " AND idActividad LIKE %s"
        params.append('%' + actividad + '%')

    if costo:
        query += " AND costo LIKE %s"
        params.append('%' + costo + '%')

    # Ejecutar la consulta
    cursor.execute(query, params)
    equipamiento_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Pasar los resultados a la plantilla
    return render_template('equipamiento.html', equipamiento=equipamiento_result)

@app.route('/buscar_clases', methods=['POST'])
def buscar_clases():
    # Obtener los valores del formulario
    nombre = request.form.get('nombre', '').strip()
    actividad_clase = request.form.get('actividad_clase', '').strip()
    turno = request.form.get('turno', '').strip()
    dictada = request.form.get('dictada', '').strip()

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    # Consulta base
    query = "select idClase, idTurno, dictada, descripcion, nombre"
    query += " FROM clase"
    query += " inner join actividades a on clase.idActividad = a.idActividad"
    query += " inner join instructores i on clase.ciInstructor = i.ciInstructor"
    query += " WHERE 1=1"

    params = []

    # Agregar condiciones dinámicas si los campos no están vacíos
    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')

    if actividad_clase:
        query += " AND a.descripcion LIKE %s"
        params.append('%' + actividad_clase + '%')

    if turno:
        query += " AND IdTurno LIKE %s"
        params.append('%' + turno + '%')

    if dictada:
        query += " AND dictada LIKE %s"
        params.append('%' + dictada + '%')

    # Ejecutar la consulta
    cursor.execute(query, params)
    clases_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Pasar los resultados a la plantilla
    return render_template('clase.html', clases=clases_result)

@app.route('/eliminar_alumno/<int:ciAlumno>', methods=['POST'])
def eliminar_alumno(ciAlumno):
    print(f"Eliminando alumno con CI: {ciAlumno}")  # Añadir para depurar
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "DELETE FROM alumnos WHERE ciAlumno = %s"
    cursor.execute(query, (ciAlumno,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('alumnos_page'))

@app.route('/editar_alumno', methods=['POST'])
def editar_alumno():
    ciAlumno = request.form['ciAlumno']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    alquila = request.form['alquila']

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor()

    if alquila.lower() == "0":
        alquila = 0 # 'true' o '1' se convierte a 1
    else:
        alquila = 1

    # Actualizar la información del alumno en la base de datos
    # Actualizar la información del alumno en la base de datos
    query = "UPDATE alumnos"
    query += " SET nombre = %s, apellido = %s, alquila = %s"
    query += " WHERE ciAlumno = %s"

    # Asegúrate de que también pases 'ciAlumno' como parámetro
    cursor.execute(query, (nombre, apellido, alquila, ciAlumno))

    cnx.commit()

    # Cerrar la conexión y redirigir de nuevo a la página de alumnos
    cursor.close()
    cnx.close()

    return redirect(url_for('alumnos_page'))

@app.route('/eliminar_equipamiento/<int:ciAlumno>', methods=['POST'])
def eliminar_equipamiento(idEquipamiento):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "DELETE FROM equipamiento WHERE idEquipamiento = %s"
    cursor.execute(query, (idEquipamiento,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('equipamiento_page'))

@app.route('/editar_equipamiento', methods=['POST'])
def editar_equipamiento():
    idEquipamiento = request.form['idEquipamiento']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    actividad = request.form['y']

    # Conectar a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor()

    if alquila.lower() == "0":
        alquila = 0 # 'true' o '1' se convierte a 1
    else:
        alquila = 1

    # Actualizar la información del alumno en la base de datos
    # Actualizar la información del alumno en la base de datos
    query = "UPDATE alumnos"
    query += " SET nombre = %s, apellido = %s, alquila = %s"
    query += " WHERE ciAlumno = %s"

    # Asegúrate de que también pases 'ciAlumno' como parámetro
    cursor.execute(query, (nombre, apellido, alquila, ciAlumno))

    cnx.commit()

    # Cerrar la conexión y redirigir de nuevo a la página de alumnos
    cursor.close()
    cnx.close()

    return redirect(url_for('equipamiento_page'))


if __name__ == '__main__':
    app.run(debug=True)
