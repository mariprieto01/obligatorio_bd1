from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# Función para obtener la conexión a la base de datos
def get_db_connection():
    cnx = mysql.connector.connect(user='root', password='obligatorio', host='db', database='obligatorio')
    return cnx

# Ejemplo de uso: Realizar una consulta simple
def ejemplo_consulta():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM usuario"
    cursor.execute(query)
    for el in cursor:
        print(el)
    cnx.close()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Aquí puedes manejar la lógica para registrar al usuario
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET','POST'])
def do_login():
    # Aquí puedes agregar la lógica para verificar el inicio de sesión
    # Por ahora, solo redirigiremos a la página de pestañas
    return redirect(url_for('tabs'))

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
        usuario = request.form['usuario']
        nueva_contrasena = request.form['nueva-contrasena']
        confirmar_contrasena = request.form['confirmarContrasena']

        if nueva_contrasena == confirmar_contrasena:
            return redirect(url_for('login', mensaje='Contraseña cambiada exitosamente'))
        else:
            return redirect(url_for('cambiar_contrasena', mensaje='Las contraseñas no coinciden'))

    mensaje = request.args.get('mensaje')
    return render_template('cambiarContraseña.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
    ejemplo_consulta()
