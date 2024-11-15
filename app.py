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
        query = "SELECT * FROM login WHERE correo = %s AND password = %s"
        cursor.execute(query, (email, password))
        email = cursor.fetchone()
        cursor.close()
        cnx.close()

        if email:
            return redirect(url_for('tabs'))
        else:
            return render_template('login.html', error="email o contraseña incorrectos.")
    return render_template('login.html')

@app.route('/pestañas', methods=['GET', 'POST'])
def tabs():
    resultados = []
    equipamiento_resultados = []

    # Conexión a la base de datos
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)

    if request.method == 'POST':
        # Procesar búsqueda en la sección de Alumnos
        if 'nombre' in request.form or 'apellido' in request.form or 'actividad' in request.form or 'alquila' in request.form:
            nombre = request.form.get('nombre', '')
            apellido = request.form.get('apellido', '')
            actividad = request.form.get('actividad', '')
            alquila = request.form.get('alquila', '')

            query = "SELECT * FROM alumnos WHERE 1=1"
            params = []
            if nombre:
                query += " AND nombre LIKE %s"
                params.append(f"%{nombre}%")
            if apellido:
                query += " AND apellido LIKE %s"
                params.append(f"%{apellido}%")
            if actividad:
                query += " AND actividad LIKE %s"
                params.append(f"%{actividad}%")
            if alquila:
                query += " AND alquila LIKE %s"
                params.append(f"%{alquila}%")

            cursor.execute(query, params)
            resultados = cursor.fetchall()

        # Procesar búsqueda en la sección de Equipamiento
        elif 'tipo' in request.form or 'estado' in request.form or 'talle' in request.form:
            tipo = request.form.get('tipo', '')
            estado = request.form.get('estado', '')
            talle = request.form.get('talle', '')

            query = "SELECT * FROM equipamiento WHERE 1=1"
            params = []
            if tipo:
                query += " AND tipo LIKE %s"
                params.append(f"%{tipo}%")
            if estado:
                query += " AND estado LIKE %s"
                params.append(f"%{estado}%")
            if talle:
                query += " AND talle LIKE %s"
                params.append(f"%{talle}%")

            cursor.execute(query, params)
            equipamiento_resultados = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('pestañas.html',
                           resultados=resultados,
                           equipamiento_resultados=equipamiento_resultados,
                           request=request)

if __name__ == '__main__':
    app.run(debug=True)
