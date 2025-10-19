from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def inicio():
    return render_template('inicio.html')


#@app.route('/ruta del url)
#def nombre funcion llamada en href del layout
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


@app.route('/rentas_patentes')
def rentas_patentes():
    return render_template('rentas_patentes.html')


@app.route('/transito')
def transito():
    return render_template('transito.html')

@app.route('/juzgado_policia_local')
def policia():
    return render_template('policia.html')


@app.route('/organigrama')
def organigrama():
    return render_template('organigrama.html')


@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/himno')
def himno():
    return render_template('himno.html')

@app.route('/org_comunitarias')
def org_comunitarias():
    return render_template('org_comunitarias.html')

@app.route('/concursos')
def concursos():
    return render_template('concursos.html')

@app.route('/noticias')
def noticias():
    # Aquí normalmente irías a la base de datos a buscar las noticias
    return render_template('noticias.html')

@app.route('/telefonos')
def telefonos():
    # Datos para las cards de teléfonos principales
    telefonos_principales = [
        {
            "titulo": "MESA CENTRAL (OTRO)",
            "numero": "+45 288 9001",
            "icono": "bi-telephone-fill",
            "color": "primary"
        },
        {
            "titulo": "CESFAM FREIRE",
            "numero": "45 288 9276",
            "icono": "bi-hospital",
            "color": "success"
        },
        {
            "titulo": "SAPU - EMERGENCIAS LAS: CESFAM FREIRE",
            "numero": "45 288 9257",
            "icono": "bi-ambulance",
            "color": "danger"
        },
        {
            "titulo": "CESFAM QUINTO",
            "numero": "45 288 9327",
            "icono": "bi-house-heart",
            "color": "info"
        },
        {
            "titulo": "SAPY FREIRE - Avda. Balmaceda",
            "numero": "45 288 9328",
            "icono": "bi-clipboard2-pulse",
            "color": "warning"
        },
        {
            "titulo": "SAPU - CESFAM EL BOSQUE",
            "numero": "45 288 9342",
            "icono": "bi-ambulance",
            "color": "danger"
        },
        {
            "titulo": "SAPU - CESFAM QUINTO",
            "numero": "45 288 9321",
            "icono": "bi-ambulance",
            "color": "danger"
        }
    ]

    # Datos para la tabla del directorio telefónico
    directorio_telefonico = [
        {"numero": "452889066", "dependencia": "ENCARGADA BIBLIOTECA FREIRE", "ubicacion": "FREIRE", "departamento": "BIBLIOTECA"},
        {"numero": "452889067", "dependencia": "ENCARGADA BIBLIOTECA", "ubicacion": "FREIRE", "departamento": "BIBLIOTECA"},
        {"numero": "452889075", "dependencia": "ENCARGADA BIBLIOTECA QUINTO", "ubicacion": "QUINTO", "departamento": "BIBLIOTECA"},
        {"numero": "452889016", "dependencia": "PROFESORA, DIRECTORA DE GESTIÓN, PEDAGOGÍA Y CURRÍCULO", "ubicacion": "FREIRE", "departamento": "EDUCACIÓN"},
        {"numero": "452889059", "dependencia": "ENCARGADA BODEGA MUNICIPAL, ORG. TERRITORIAL", "ubicacion": "FREIRE", "departamento": "MUNICIPAL"},
        {"numero": "452889061", "dependencia": "ADMINISTRATIVO BÁSICO, MUNICIPAL, MANTENCIÓN ARENA", "ubicacion": "FREIRE", "departamento": "MUNICIPAL"},
        {"numero": "452889096", "dependencia": "PROGRAMA EMBARAZADA, ERICO NUEVA", "ubicacion": "FREIRE", "departamento": "SALUD"},
        {"numero": "452889340", "dependencia": "ODONTOLOGÍA, NUEVA IMPLEMENTACIÓN", "ubicacion": "FREIRE", "departamento": "SALUD"},
        {"numero": "452889341", "dependencia": "FARMACIA TRATTA MUNICIPAL", "ubicacion": "FREIRE", "departamento": "SALUD"},
        {"numero": "452889342", "dependencia": "SAPU, TURNO VERGARA - FERNANDO SOTO", "ubicacion": "FREIRE", "departamento": "SALUD"}
    ]

    return render_template('telefonos.html', 
                         telefonos_principales=telefonos_principales,
                         directorio_telefonico=directorio_telefonico)

if __name__ == '__main__':
    app.run(debug=True)