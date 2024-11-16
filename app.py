from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        cnx = mysql.connector.connect(user='root', password='obligatorio', host='127.0.0.1', database='obligatorio')
        return cnx
    except mysql.connector.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

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

        if not (nombre and apellido and email and password):
            return render_template('registro.html', error="Todos los campos son obligatorios.")

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor()
                query = "INSERT INTO login (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, apellido, email, password))
                cnx.commit()
                cursor.close()
                cnx.close()
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('registro.html', error=f"Error al registrar: {e}")

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not (email and password):
            return render_template('login.html', error="Todos los campos son obligatorios.")

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor()
                query = "SELECT * FROM login WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                cursor.close()
                cnx.close()

                if user:
                    return redirect(url_for('alumnos'))
                else:
                    return render_template('login.html', error="Email o contraseña incorrectos.")
        except Exception as e:
            return render_template('login.html', error=f"Error al iniciar sesión: {e}")

    return render_template('login.html')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        apellido = request.form.get('apellido', '')
        actividad = request.form.get('actividad', '')
        alquila = request.form.get('alquila', '')

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor(dictionary=True)
                query = "SELECT ciAlumno, nombre, apellido, fecha_nacimiento, idActividad, alquila FROM alumnos WHERE 1=1"
                params = []

                if nombre:
                    query += " AND nombre LIKE %s"
                    params.append(f"%{nombre}%")
                if apellido:
                    query += " AND apellido LIKE %s"
                    params.append(f"%{apellido}%")
                if actividad:
                    query += " AND idActividad LIKE %s"
                    params.append(f"%{actividad}%")
                if alquila:
                    query += " AND alquila LIKE %s"
                    params.append(f"%{alquila}%")

                cursor.execute(query, params)
                alumnos_result = cursor.fetchall()
                cursor.close()
                cnx.close()

                return render_template('pestañas.html', alumnos=alumnos_result)
        except Exception as e:
            return render_template('pestañas.html', error=f"Error al obtener alumnos: {e}")

    return render_template('pestañas.html')

@app.route('/equipamiento', methods=['GET', 'POST'])
def equipamiento():
    if request.method == 'POST':
        id = request.form.get('id', '').strip()
        actividad = request.form.get('actividad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        costo = request.form.get('costo', '').strip()

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor(dictionary=True)
                query = "SELECT idEquipamiento, idActividad, descripcion, costo FROM equipamiento WHERE 1=1"
                params = []

                if id:
                    query += " AND idEquipamiento LIKE %s"
                    params.append(f"%{id}%")
                if actividad:
                    query += " AND idActividad LIKE %s"
                    params.append(f"%{actividad}%")
                if descripcion:
                    query += " AND descripcion LIKE %s"
                    params.append(f"%{descripcion}%")
                if costo:
                    query += " AND costo LIKE %s"
                    params.append(f"%{costo}%")

                cursor.execute(query, params)
                equipamiento_result = cursor.fetchall()
                cursor.close()
                cnx.close()

                return render_template('pestañas.html', equipamientos=equipamiento_result)
        except Exception as e:
            return render_template('pestañas.html', error=f"Error al obtener equipamiento: {e}")

    return render_template('pestañas.html')

@app.route('/instructor', methods=['GET', 'POST'])
def instructor():
    if request.method == 'POST':
        ci = request.form.get('ci')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor(dictionary=True)
                query = """
                SELECT ciInstructor, nombre, apellido
                FROM instructor
                WHERE 1=1
                """
                params = []

                if ci:
                    query += " AND ciInstructor LIKE %s"
                    params.append(f"%{ci}%")
                if nombre:
                    query += " AND nombre LIKE %s"
                    params.append(f"%{nombre}%")
                if apellido:
                    query += " AND apellido LIKE %s"
                    params.append(f"%{apellido}%")

                cursor.execute(query, params)
                instructores_result = cursor.fetchall()
                cursor.close()
                cnx.close()

                return render_template('pestañas.html', instructores=instructores_result)
        except Exception as e:
            return render_template('pestañas.html', error=f"Error al obtener instructores: {e}")

    return render_template('pestañas.html')


@app.route('/clases', methods=['GET', 'POST'])
def clases():
    if request.method == 'POST':
        id_instructor = request.form.get('ciInstructor')
        actividad = request.form.get('idActividad')
        turno = request.form.get('turno')
        dictada = request.form.get('dictada')

        try:
            cnx = get_db_connection()
            if cnx:
                cursor = cnx.cursor(dictionary=True)
                query = """
                    SELECT * FROM clases
                    WHERE (idInstructor = %s OR %s IS NULL)
                    AND (idActividad LIKE %s OR %s IS NULL)
                    AND (idTurno = %s OR %s IS NULL)
                    AND (dictada = %s OR %s IS NULL)
                """
                cursor.execute(query, (
                    id_instructor, id_instructor,
                    f"%{actividad}%", actividad,
                    turno, turno,
                    dictada, dictada
                ))
                clases_result = cursor.fetchall()
                cursor.close()
                cnx.close()

                return render_template('pestañas.html', clases=clases_result)
        except Exception as e:
            print(f"Error: {e}")

    return render_template('pestañas.html')

if __name__ == '__main__':
    app.run(debug=True)
