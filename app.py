from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    cnx = mysql.connector.connect(user='root', password='obligatorio', host='127.0.0.1', database='obligatorio')
    return cnx

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/alumnos')
def alumnos_page():
    return render_template('alumnos.html')

@app.route('/alumnoClase')
def alumno_clase_page():
    return render_template('alumnoClase.html')

@app.route('/asignar_rol')
def asignar_rol_page():
    return render_template('asignar_rol.html')

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
        INSERT INTO login (nombre, apellido, email, password, rol)
        VALUES (%s, %s, %s, %s, null)
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

        print(f"Email recibido: {email}")
        print(f"Contraseña recibida: {password}")

        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "SELECT nombre, rol, email FROM login WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        email = cursor.fetchone()
        cursor.close()
        cnx.close()
        print(f"Resultado de la consulta: {email}")
        if email:
            rol = email[1]
            if rol == 'administrador':
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="email o contraseña incorrectos.")
    return render_template('login.html')

@app.route('/buscar_instructores', methods=['POST'])
def buscar_instructores():
    nombre = request.form.get('nombreInstructor', '').strip()
    apellido = request.form.get('apellidoInstructor', '').strip()
    ci = request.form.get('ci', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT ciInstructor, nombre, apellido"
    query += " FROM instructores"
    query += " WHERE 1=1"
    params = []

    if ci:
        query += " AND ciInstructor LIKE %s"
        params.append('%' + ci + '%')

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')

    if apellido:
        query += " AND apellido LIKE %s"
        params.append('%' + apellido + '%')

    cursor.execute(query, params)
    instructores_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('instructores.html', instructores=instructores_result)

@app.route('/buscar_alumnos', methods=['POST'])
def buscar_alumnos():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT ciAlumno, nombre, apellido, fecha_nacimiento"
    query += " FROM alumnos"
    query += " WHERE 1=1"
    params = []

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')

    if apellido:
        query += " AND apellido LIKE %s"
        params.append('%' + apellido + '%')

    cursor.execute(query, params)
    alumnos_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('alumnos.html', alumnos=alumnos_result)

@app.route('/buscar_equipamiento', methods=['POST'])
def buscar_equipamiento():
    id = request.form.get('id', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    actividad = request.form.get('actividad', '').strip()
    costo = request.form.get('costo', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT idEquipamiento, descripcion, costo, idActividad"
    query += " FROM equipamiento"
    query += " WHERE 1=1"
    params = []

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

    cursor.execute(query, params)
    equipamiento_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('equipamiento.html', equipamiento=equipamiento_result)

@app.route('/buscar_clases', methods=['POST'])
def buscar_clases():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    actividad_clase = request.form.get('actividad_clase', '').strip()
    idTurno = request.form.get('idTurno', '').strip()
    dictada = request.form.get('dictada', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT idClase, idTurno, dictada, descripcion, nombre, apellido"
    query += " FROM clase"
    query += " INNER JOIN actividades a ON clase.idActividad = a.idActividad"
    query += " INNER JOIN instructores i ON clase.ciInstructor = i.ciInstructor"
    query += " WHERE 1=1"

    params = []

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%' + apellido + '%')

    if actividad_clase:
        query += " AND a.descripcion LIKE %s"
        params.append('%' + actividad_clase + '%')

    if idTurno:
        query += " AND idTurno LIKE %s"
        params.append('%' + idTurno + '%')

    if dictada:
        query += " AND dictada LIKE %s"
        params.append('%' + dictada + '%')

    cursor.execute(query, params)
    clases_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('clase.html', clases=clases_result)

@app.route('/asignar_rol', methods=['GET', 'POST'])
def asignar_rol():
    if request.method == 'POST':
        nombre = request.form['txt']
        email = request.form['email']
        rol = request.form['rol']

        cnx = get_db_connection()
        cursor = cnx.cursor()
        print(f"Nombre: {nombre}, Email: {email}, Rol: {rol}")

        query = "UPDATE login"
        query += " SET rol = %s"
        query += " WHERE nombre = %s AND email = %s"

        cursor.execute(query, (rol, nombre, email))
        cnx.commit()

        cursor.close()
        cnx.close()

        return render_template('asignar_rol.html', success="Rol asignado correctamente.")

    return render_template('asignar_rol.html')

@app.route('/alumno_nuevo', methods=['POST'])
def alumno_nuevo():
    ciAlumno = request.form.get('ciAlumno')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    fecha_nacimiento = request.form.get('fecha_nacimiento')

    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM alumnos WHERE ciAlumno = %s"
    cursor.execute(check_query, (ciAlumno,))
    alumnoExistente = cursor.fetchone()

    if alumnoExistente:
        cursor.close()
        cnx.close()
        return render_template('nuevoAlumno.html', error="El alumno con esta CI ya existe en la base de datos.")

    query = """
        INSERT INTO alumnos (ciAlumno, nombre, apellido, fecha_nacimiento)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (ciAlumno, nombre, apellido, fecha_nacimiento))
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('nuevoAlumno.html', success="Alumno creado con éxito.")

@app.route('/instructor_nuevo', methods=['POST'])
def instructor_nuevo():
    ciInstructor = request.form.get('ciInstructor')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')


    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM instructores WHERE ciInstructor = %s"
    cursor.execute(check_query, (ciInstructor,))
    instructorExistente = cursor.fetchone()

    if instructorExistente:
        cursor.close()
        cnx.close()
        return render_template('nuevoInstructor.html', error="El instructor con esta CI ya existe en la base de datos.")

    query = """
        INSERT INTO instructores (ciInstructor, nombre, apellido)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (ciInstructor, nombre, apellido))
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('nuevoInstructor.html', success="Instructor creado con éxito.")

@app.route('/clase_nueva', methods=['POST'])
def clase_nueva():
    idClase = request.form.get('idClase')
    ciInstructor = request.form.get('ciInstructor')
    idActividad = request.form.get('idActividad')
    idTurno = request.form.get('idTurno')
    dictada = request.form.get('dictada').strip()

    if dictada == 'sí':
        dictada = 1
    else:
        dictada = 0

    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM clase WHERE idClase = %s"
    cursor.execute(check_query, (idClase,))
    claseExistente = cursor.fetchone()

    if claseExistente:
        cursor.close()
        cnx.close()
        return render_template('nuevaClase.html', error="La clase con este ID ya existe en la base de datos.")

    query = """
        INSERT INTO clase (idClase, ciInstructor, idActividad, idTurno, dictada)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (idClase, ciInstructor, idActividad, idTurno, dictada))
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('nuevaClase.html', success="Clase creada con éxito.")

@app.route('/equipamiento_nuevo', methods=['POST'])
def equipamiento_nuevo():
    idEquipamiento = request.form.get('idEquipamiento')
    idActividad = request.form.get('idActividad')
    descripcion = request.form.get('descripcion')
    costo = request.form.get('costo')

    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM equipamiento WHERE idEquipamiento = %s"
    cursor.execute(check_query, (idEquipamiento,))
    equipamientoExistente = cursor.fetchone()

    if equipamientoExistente:
        cursor.close()
        cnx.close()
        return render_template('nuevoEquipamiento.html', error="El equipamiento con este ID ya existe en la base de datos.")

    query = """
        INSERT INTO equipamiento (idEquipamiento, descripcion, costo, idActividad)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (idEquipamiento, descripcion, costo, idActividad))
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('nuevoEquipamiento.html', success="Equipamiento creado con éxito.")

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
    fecha_nacimiento = request.form['fecha_nacimiento']

    print(ciAlumno, nombre, apellido, fecha_nacimiento)  # Depuración

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE alumnos
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s
        WHERE ciAlumno = %s
    """

    cursor.execute(query, (nombre, apellido, fecha_nacimiento, ciAlumno))

    cnx.commit()
    cursor.close()
    cnx.close()

    return redirect(url_for('alumnos_page'))

@app.route('/eliminar_equipamiento/<int:idEquipamiento>', methods=['POST'])
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
    idEquipamiento = request.form['idModal']  # Asegúrate de que este campo esté en el formulario
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    actividad = request.form['actividad']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = "UPDATE equipamiento"
    query += " SET descripcion = %s, costo = %s, idActividad = %s"
    query += " WHERE idEquipamiento = %s"
    cursor.execute(query, (descripcion, costo, actividad, idEquipamiento))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('equipamiento_page'))

@app.route('/eliminar_clase/<int:idClase>', methods=['POST'])
def eliminar_clase(idClase):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "DELETE FROM clase WHERE idClase = %s"
    cursor.execute(query, (idClase,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('clase_page'))

@app.route('/editar_clase', methods=['POST'])
def editar_clase():
    idClase = request.form['idClase']
    ciInstructor = request.form['ciInstructor']
    idActividad = request.form['descripcion']
    idTurno = request.form['idTurno']
    dictada = request.form['dictada']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    if dictada == 'sí':
        dictada = 1
    else:
        dictada = 0

    query = "UPDATE clase"
    query += " SET ciInstructor = %s, idActividad = %s, idTurno = %s, dictada = %s"
    query += " WHERE idClase = %s"

    cursor.execute(query, (ciInstructor, idActividad, idTurno, dictada, idClase))
    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('clase_page'))

@app.route('/eliminar_instructor/<int:ciInstructor>', methods=['POST'])
def eliminar_instructor(ciInstructor):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "DELETE FROM instructores WHERE ciInstructor = %s"
    cursor.execute(query, (ciInstructor,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('instructores_page'))

@app.route('/editar_instructor', methods=['POST'])
def editar_instructor():
    nombreInstructor = request.form['nombre']
    apellidoInstructor = request.form['apellido']
    ci = request.form['ciInstructor']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = "UPDATE instructores"
    query += " SET nombre = %s, apellido = %s"
    query += " WHERE ciInstructor = %s"

    cursor.execute(query, (nombreInstructor, apellidoInstructor, ci))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('instructores_page'))

@app.route('/reporte', methods=['GET'])
def reporte():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    ingresos_query = """
        SELECT a.descripcion AS actividad, SUM(e.costo) AS ingresos
        FROM actividades a
        JOIN equipamiento e ON a.idActividad = e.idActividad
        JOIN alumno_clase ac ON e.idEquipamiento = ac.idEquipamiento
        GROUP BY a.descripcion
        ORDER BY ingresos DESC;
    """
    cursor.execute(ingresos_query)
    ingresos = cursor.fetchall()

    alumnos_query = """
        SELECT a.descripcion AS actividad, COUNT(DISTINCT ac.ciAlumno) AS cantidad_alumnos
        FROM actividades a
        JOIN clase c ON a.idActividad = c.idActividad
        JOIN alumno_clase ac ON c.idClase = ac.idClase
        GROUP BY a.descripcion
        ORDER BY cantidad_alumnos DESC;
    """
    cursor.execute(alumnos_query)
    alumnos = cursor.fetchall()

    turnos_query = """
            SELECT t.idTurno AS turno, t.hora_inicio AS inicio, t.hora_fin AS fin, COUNT(c.idClase) AS clases_dictadas
            FROM turnos t
            JOIN clase c ON t.idTurno = c.idTurno
            WHERE c.dictada = 1
            GROUP BY t.idTurno, t.hora_inicio, t.hora_fin
            ORDER BY clases_dictadas DESC;
        """
    cursor.execute(turnos_query)
    turnos = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('reporte.html', ingresos=ingresos, alumnos=alumnos, turnos=turnos)

@app.route('/actividades', methods=['GET'])
def actividades():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT * FROM actividades"
    cursor.execute(query)
    actividades = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('actividades.html', actividades=actividades)

@app.route('/eliminar_actividad/<int:idActividad>', methods=['POST'])
def eliminar_actividad(idActividad):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = "DELETE FROM actividades WHERE idActividad = %s"
    cursor.execute(query, (idActividad,))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('actividades'))

@app.route('/editar_actividad', methods=['POST'])
def editar_actividad():
    idActividad = request.form['idActividad']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    restriccionEdad = request.form['restriccionEdad']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = "UPDATE actividades"
    query += " SET descripcion = %s, costo = %s, restriccionEdad = %s"
    query += " WHERE idActividad = %s"

    cursor.execute(query, (descripcion, costo, restriccionEdad, idActividad))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('actividades'))

@app.route('/actividad_nueva', methods=['POST'])
def actividad_nueva():
    idActividad = request.form['idActividad']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    restriccionEdad = request.form['restriccionEdad']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM actividades WHERE idActividad = %s"
    cursor.execute(check_query, (idActividad,))
    actividadExistente = cursor.fetchone()

    if actividadExistente:
        cursor.close()
        cnx.close()
        return redirect(url_for('actividades', error="La actividad con este ID ya existe en la base de datos."))

    query = """
        INSERT INTO actividades (idActividad, descripcion, costo, restriccionEdad)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (idActividad, descripcion, costo, restriccionEdad))
    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('actividades', success="Actividad eliminada con éxito"))

@app.route('/nuevaActividad')
def nueva_actividad():
    return render_template('nuevaActividad.html')

@app.route('/turnos', methods=['GET'])
def mostrar_turnos():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM turnos")
    turnos = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('turnos.html', turnos=None)

@app.route('/buscar_turno', methods=['POST'])
def buscar_turno():
    id_turno = request.form.get('idTurno', '').strip()
    hora_inicio = request.form.get('horaInicio', '').strip()
    hora_fin = request.form.get('horaFin', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT * FROM turnos WHERE 1=1"
    params = []

    if id_turno:
        query += " AND idTurno LIKE %s"
        params.append('%' + id_turno + '%')

    if hora_inicio:
        query += " AND hora_inicio LIKE %s"
        params.append('%' + hora_inicio + '%')

    if hora_fin:
        query += " AND hora_fin LIKE %s"
        params.append('%' + hora_fin + '%')

    cursor.execute(query, params)
    turnos_result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('turnos.html', turnos=turnos_result)

@app.route('/editar_turno', methods=['POST'])
def editar_turno():
    idTurno = request.form['idModal']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE turnos
        SET hora_inicio = %s, hora_fin = %s
        WHERE idTurno = %s
    """
    cursor.execute(query, (hora_inicio, hora_fin, idTurno))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('mostrar_turno'))

@app.route('/nuevo_turno', methods=['GET', 'POST'])
def nuevo_turno():
    if request.method == 'GET':
        return render_template('nuevoTurno.html')

    idTurno = request.form.get('idTurno')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    if not idTurno or not hora_inicio or not hora_fin:
        return render_template('nuevoTurno.html', error="Todos los campos son obligatorios.")

    cnx = get_db_connection()
    cursor = cnx.cursor()

    check_query = "SELECT * FROM turnos WHERE idTurno = %s"
    cursor.execute(check_query, (idTurno,))
    turno_existente = cursor.fetchone()

    if turno_existente:
        cursor.close()
        cnx.close()
        return render_template('nuevoTurno.html', error="El turno con este ID ya existe en la base de datos.")

    query = """
        INSERT INTO turnos (idTurno, hora_inicio, hora_fin)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (idTurno, hora_inicio, hora_fin))
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('nuevoTurno.html', success="Turno creado con éxito.")

@app.route('/eliminar_turno/<int:idTurno>', methods=['POST'])
def eliminar_turno(idTurno):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = "DELETE FROM turnos WHERE idTurno = %s"
    cursor.execute(query, (idTurno,))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('mostrar_turnos'))

@app.route('/alumnoClase', methods=['GET'])
def mostrar_alumnos_clase():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM alumno_clase")
    alumnos_clase = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('alumnoClase.html', alumnos_clase=alumnos_clase)

@app.route('/buscar_alumno_clase', methods=['POST'])
def buscar_alumno_clase():
    id_clase = request.form.get('idClase', '').strip()
    ci_alumno = request.form.get('ciAlumno', '').strip()
    id_equipamiento = request.form.get('idEquipamiento', '').strip()

    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT * FROM alumno_clase WHERE 1=1"
    params = []

    if id_clase:
        query += " AND idClase = %s"
        params.append(id_clase)

    if ci_alumno:
        query += " AND ciAlumno = %s"
        params.append(ci_alumno)

    if id_equipamiento:
        query += " AND idEquipamiento = %s"
        params.append(id_equipamiento)

    cursor.execute(query, params)
    alumnos_result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('alumnoClase.html', alumno_clase=alumnos_result)

@app.route('/editar_alumno_clase', methods=['POST'])
def editar_alumno_clase():
    id_clase = request.form['idClase']
    ci_alumno = request.form['ciAlumno']
    id_equipamiento = request.form.get('idEquipamiento')

    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE alumno_clase
        SET idEquipamiento = %s
        WHERE idClase = %s AND ciAlumno = %s
    """
    cursor.execute(query, (id_equipamiento, id_clase, ci_alumno))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('mostrar_alumnos_clase'))

@app.route('/nuevo_alumno_clase', methods=['GET', 'POST'])
def nuevo_alumno_clase():
    if request.method == 'POST':
        idClase = request.form.get('idClase')
        ciAlumno = request.form.get('ciAlumno')
        idEquipamiento = request.form.get('idEquipamiento') or None

        if not idClase or not ciAlumno:
            return render_template('nuevoAlumnoClase.html', error="Todos los campos son obligatorios.")

        cnx = get_db_connection()
        cursor = cnx.cursor()

        check_clase_query = "SELECT * FROM clase WHERE idClase = %s"
        cursor.execute(check_clase_query, (idClase,))
        clase_existente = cursor.fetchone()

        if not clase_existente:
            cursor.close()
            cnx.close()
            return render_template('nuevoAlumnoClase.html', error="La clase con este ID no existe.")

        check_alumno_query = "SELECT * FROM alumnos WHERE ciAlumno = %s"
        cursor.execute(check_alumno_query, (ciAlumno,))
        alumno_existente = cursor.fetchone()

        if not alumno_existente:
            cursor.close()
            cnx.close()
            return render_template('nuevoAlumnoClase.html', error="El alumno con esta cédula no existe.")

        check_query = "SELECT * FROM alumno_clase WHERE idClase = %s AND ciAlumno = %s"
        cursor.execute(check_query, (idClase, ciAlumno))
        alumno_existente_en_clase = cursor.fetchone()

        if alumno_existente_en_clase:
            cursor.close()
            cnx.close()
            return render_template('nuevoAlumnoClase.html', error="El alumno ya está inscripto en esta clase.")

        query = """
            INSERT INTO alumno_clase (idClase, ciAlumno, idEquipamiento)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (idClase, ciAlumno, idEquipamiento))
        cnx.commit()

        cursor.close()
        cnx.close()

        return render_template('nuevoAlumnoClase.html', success="Alumno añadido a la clase con éxito.")

    return render_template('nuevoAlumnoClase.html')

@app.route('/eliminar_alumno_clase/<ciAlumno>/<idClase>', methods=['POST'])
def eliminar_alumno_clase(ciAlumno, idClase):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    try:
        query = "DELETE FROM alumno_clase WHERE ciAlumno = %s AND idClase = %s"
        cursor.execute(query, (ciAlumno, idClase))
        cnx.commit()
    except Exception as e:
        print(f"Error al eliminar el registro: {e}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('mostrar_alumnos_clase'))

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