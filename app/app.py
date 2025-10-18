from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/alcalde')
def alcalde():
    return render_template('alcalde.html')

@app.route('/consejo_municipal')
def consejo_municipal():
    # Datos de ejemplo para los concejales
    concejales = [
        {
            "nombre": "Luis Figueroa Loncón", 
            "cargo": "Concejal", 
            "imagen": "consejal1.png",
            "partido": "Partido A",
            "comisiones": ["Educación", "Salud"],
            "biografia": "Concejal con 8 años de experiencia en el cargo..."
        },
        {
            "nombre": "Marcelo Riveros Briones", 
            "cargo": "Concejal", 
            "imagen": "consejal2.png",
            "partido": "Partido B",
            "comisiones": ["Obras Públicas", "Medio Ambiente"],
            "biografia": "Profesional con amplia trayectoria en gestión pública..."
        },
        {
            "nombre": "Luis García Friz", 
            "cargo": "Concejal", 
            "imagen": "consejal3.png",
            "partido": "Partido C",
            "comisiones": ["Seguridad", "Deportes"],
            "biografia": "Ex deportista comprometido con el desarrollo comunal..."
        },
        {
            "nombre": "Marcos Colicoi Berna", 
            "cargo": "Concejal", 
            "imagen": "consejal4.png",
            "partido": "Partido A",
            "comisiones": ["Cultura", "Turismo"],
            "biografia": "Promotora cultural con 10 años de servicio..."
        },
        {
            "nombre": "José Inostroza Corral", 
            "cargo": "Concejal", 
            "imagen": "consejal5.png",
            "partido": "Partido B",
            "comisiones": ["Presupuesto", "Transporte"],
            "biografia": "Economista especializado en finanzas públicas..."
        },
        {
            "nombre": "Victor Rosales Navarrete", 
            "cargo": "Concejal", 
            "imagen": "consejal6.png",
            "partido": "Partido C",
            "comisiones": ["Derechos Humanos", "Mujer y Género"],
            "biografia": "Abogada defensora de derechos humanos..."
        }
    ]
    return render_template('consejo_municipal.html', concejales=concejales)


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