from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Aquí puedes manejar la lógica para registrar al usuario
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
