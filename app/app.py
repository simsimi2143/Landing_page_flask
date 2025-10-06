from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/autoridades')
def autoridades():
    # Ejemplo de cómo pasar datos a la plantilla
    autoridades_list = [
        {"nombre": "Juan Pérez", "cargo": "Presidente", "imagen": "autoridad1.jpg"},
        {"nombre": "María García", "cargo": "Vicepresidenta", "imagen": "autoridad2.jpg"},
        {"nombre": "Carlos López", "cargo": "Secretario", "imagen": "autoridad3.jpg"}
    ]
    return render_template('autoridades.html', autoridades=autoridades_list)

@app.route('/direcciones')
def direcciones():
    return render_template('direcciones.html')

@app.route('/comuna')
def comuna():
    return render_template('comuna.html')

@app.route('/org_comunitarias')
def org_comunitarias():
    return render_template('org_comunitarias.html')

@app.route('/concursos')
def concursos():
    return render_template('concursos.html')

@app.route('/noticias')
def noticias():
    # Ejemplo de paginación con Bootstrap
    page = request.args.get('page', 1, type=int)
    # Aquí normalmente irías a la base de datos a buscar las noticias
    return render_template('noticias.html', page=page)

if __name__ == '__main__':
    app.run(debug=True)