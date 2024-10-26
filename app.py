from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Aquí puedes manejar la lógica para registrar al usuario
        # Por ejemplo, guardar los datos en una base de datos
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET','POST'])
def do_login():
    # Aquí puedes agregar la lógica para manejar el inicio de sesión
    return redirect(url_for('login'))

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
