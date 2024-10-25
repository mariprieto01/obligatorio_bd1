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

@app.route('/login', methods=['POST'])
def do_login():
    # Aquí puedes agregar la lógica para manejar el inicio de sesión
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
