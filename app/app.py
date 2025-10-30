from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from datetime import datetime

from config import Config, allowed_file
from models import db, Noticia, Alcalde, Concejal, Concurso, AdminUser,ArchivoConcurso
from forms import LoginForm, NoticiaForm, AlcaldeForm, ConcejalForm, ConcursoForm

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return AdminUser(user_id)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Crear tablas y usuario admin básico
with app.app_context():
    db.create_all()
    
    # Crear directorios de uploads si no existen
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'noticias'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'alcalde'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'concejales'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'concursos'), exist_ok=True)

# Función helper para guardar archivos
def guardar_archivo(file_data, directorio, nombre_actual=None):
    """
    Guarda un archivo si se ha subido uno nuevo
    Retorna el nombre del archivo o el nombre actual si no hay archivo nuevo
    """
    if file_data and hasattr(file_data, 'filename') and file_data.filename:
        filename = secure_filename(file_data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], directorio, filename)
        file_data.save(filepath)
        return f'uploads/{directorio}/{filename}'
    return nombre_actual

# ===== RUTAS PÚBLICAS =====
@app.route('/')
def inicio():
    # Obtener noticias activas para el carrusel
    noticias = Noticia.query.filter_by(activa=True).order_by(Noticia.fecha_publicacion.desc()).limit(6).all()
    return render_template('inicio.html', noticias=noticias)

@app.route('/alcalde')
def alcalde():
    alcalde_info = Alcalde.query.first()
    return render_template('alcalde.html', alcalde=alcalde_info)

@app.route('/consejo_municipal')
def consejo_municipal():
    concejales = Concejal.query.filter_by(activo=True).order_by(Concejal.orden).all()
    
    # Procesar comisiones para convertir string en lista
    for concejal in concejales:
        if concejal.comisiones:
            # Convertir el string de comisiones en una lista
            concejal.comisiones_lista = [comision.strip() for comision in concejal.comisiones.split(',')]
        else:
            concejal.comisiones_lista = []
    
    return render_template('consejo_municipal.html', concejales=concejales)


@app.route('/concursos')
def concursos():
    concursos_list = Concurso.query.filter_by(activo=True).order_by(Concurso.fecha.desc()).all()
    
    # Para cada concurso, obtener sus archivos
    for concurso in concursos_list:
        concurso.archivos = ArchivoConcurso.query.filter_by(concurso_id=concurso.id).all()
    
    return render_template('concursos.html', concursos=concursos_list)

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

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/telefonos')
def telefonos():
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
        }
    ]

    directorio_telefonico = [
        {"numero": "452889066", "dependencia": "ENCARGADA BIBLIOTECA FREIRE", "ubicacion": "FREIRE", "departamento": "BIBLIOTECA"},
        {"numero": "452889067", "dependencia": "ENCARGADA BIBLIOTECA", "ubicacion": "FREIRE", "departamento": "BIBLIOTECA"},
        {"numero": "452889075", "dependencia": "ENCARGADA BIBLIOTECA QUINTO", "ubicacion": "QUINTO", "departamento": "BIBLIOTECA"}
    ]

    return render_template('telefonos.html', 
                         telefonos_principales=telefonos_principales,
                         directorio_telefonico=directorio_telefonico)

# ===== RUTAS DE ADMINISTRACIÓN =====
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if (form.username.data == app.config['ADMIN_USERNAME'] and 
            form.password.data == app.config['ADMIN_PASSWORD']):
            user = AdminUser(1)
            login_user(user)
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/')
@login_required
def admin_dashboard():
    stats = {
        'noticias': Noticia.query.count(),
        'concejales': Concejal.query.count(),
        'concursos': Concurso.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# ===== GESTIÓN DE NOTICIAS =====
@app.route('/admin/noticias')
@login_required
def admin_noticias():
    noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).all()
    return render_template('admin/noticias.html', noticias=noticias)

@app.route('/admin/noticias/nueva', methods=['GET', 'POST'])
@login_required
def nueva_noticia():
    form = NoticiaForm()
    if form.validate_on_submit():
        noticia = Noticia(
            titulo=form.titulo.data,
            contenido=form.contenido.data,
            activa=form.activa.data
        )
        
        # Usar función helper para guardar imagen
        noticia.imagen = guardar_archivo(form.imagen.data, 'noticias')
        
        db.session.add(noticia)
        db.session.commit()
        flash('Noticia creada correctamente.', 'success')
        return redirect(url_for('admin_noticias'))
    
    return render_template('admin/noticia_form.html', form=form, titulo='Nueva Noticia')

@app.route('/admin/noticias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    form = NoticiaForm(obj=noticia)
    
    if form.validate_on_submit():
        noticia.titulo = form.titulo.data
        noticia.contenido = form.contenido.data
        noticia.activa = form.activa.data
        
        # Usar función helper para guardar imagen
        noticia.imagen = guardar_archivo(form.imagen.data, 'noticias', noticia.imagen)
        
        db.session.commit()
        flash('Noticia actualizada correctamente.', 'success')
        return redirect(url_for('admin_noticias'))
    
    return render_template('admin/noticia_form.html', form=form, noticia=noticia, titulo='Editar Noticia')

@app.route('/admin/noticias/eliminar/<int:id>')
@login_required
def eliminar_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    db.session.delete(noticia)
    db.session.commit()
    flash('Noticia eliminada correctamente.', 'success')
    return redirect(url_for('admin_noticias'))

# ===== GESTIÓN DEL ALCALDE =====
@app.route('/admin/alcalde', methods=['GET', 'POST'])
@login_required
def admin_alcalde():
    alcalde = Alcalde.query.first()
    form = AlcaldeForm()
    
    # Para GET, poblar el formulario con datos existentes
    if request.method == 'GET' and alcalde:
        form.nombre.data = alcalde.nombre
        form.descripcion.data = alcalde.descripcion
        form.vision.data = alcalde.vision
        form.mision.data = alcalde.mision
        form.compromisos.data = alcalde.compromisos
        form.logros.data = alcalde.logros
    
    if form.validate_on_submit():
        if not alcalde:
            alcalde = Alcalde()
        
        alcalde.nombre = form.nombre.data
        alcalde.descripcion = form.descripcion.data
        alcalde.vision = form.vision.data
        alcalde.mision = form.mision.data
        alcalde.compromisos = form.compromisos.data
        alcalde.logros = form.logros.data
        
        # Usar función helper para guardar imagen
        alcalde.imagen = guardar_archivo(form.imagen.data, 'alcalde', alcalde.imagen)
        
        if not alcalde.id:
            db.session.add(alcalde)
        
        db.session.commit()
        flash('Información del alcalde actualizada correctamente.', 'success')
        return redirect(url_for('admin_alcalde'))
    
    return render_template('admin/alcalde.html', form=form, alcalde=alcalde)

# ===== GESTIÓN DE CONCEJALES =====
@app.route('/admin/concejales')
@login_required
def admin_concejales():
    concejales = Concejal.query.order_by(Concejal.orden).all()
    return render_template('admin/concejales.html', concejales=concejales)

@app.route('/admin/concejales/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_concejal():
    form = ConcejalForm()
    if form.validate_on_submit():
        concejal = Concejal(
            nombre=form.nombre.data,
            cargo=form.cargo.data,
            partido=form.partido.data,
            comisiones=form.comisiones.data,
            biografia=form.biografia.data,
            activo=form.activo.data,
            orden=form.orden.data
        )
        
        # Usar función helper para guardar imagen
        concejal.imagen = guardar_archivo(form.imagen.data, 'concejales')
        
        db.session.add(concejal)
        db.session.commit()
        flash('Concejal creado correctamente.', 'success')
        return redirect(url_for('admin_concejales'))
    
    return render_template('admin/concejal_form.html', form=form, titulo='Nuevo Concejal')

@app.route('/admin/concejales/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_concejal(id):
    concejal = Concejal.query.get_or_404(id)
    form = ConcejalForm(obj=concejal)
    
    if form.validate_on_submit():
        concejal.nombre = form.nombre.data
        concejal.cargo = form.cargo.data
        concejal.partido = form.partido.data
        concejal.comisiones = form.comisiones.data
        concejal.biografia = form.biografia.data
        concejal.activo = form.activo.data
        concejal.orden = form.orden.data
        
        # Usar función helper para guardar imagen
        concejal.imagen = guardar_archivo(form.imagen.data, 'concejales', concejal.imagen)
        
        db.session.commit()
        flash('Concejal actualizado correctamente.', 'success')
        return redirect(url_for('admin_concejales'))
    
    return render_template('admin/concejal_form.html', form=form, concejal=concejal, titulo='Editar Concejal')

@app.route('/admin/concejales/eliminar/<int:id>')
@login_required
def eliminar_concejal(id):
    concejal = Concejal.query.get_or_404(id)
    db.session.delete(concejal)
    db.session.commit()
    flash('Concejal eliminado correctamente.', 'success')
    return redirect(url_for('admin_concejales'))

# ===== GESTIÓN DE CONCURSOS =====
@app.route('/admin/concursos')
@login_required
def admin_concursos():
    concursos = Concurso.query.order_by(Concurso.fecha.desc()).all()
    return render_template('admin/concursos.html', concursos=concursos)

@app.route('/admin/concursos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_concurso():
    form = ConcursoForm()
    if form.validate_on_submit():
        concurso = Concurso(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            fecha=form.fecha.data,
            tipo=form.tipo.data,
            activo=form.activo.data
        )
        
        db.session.add(concurso)
        db.session.flush()  # Para obtener el ID del concurso
        
        # Procesar múltiples archivos
        if form.archivos_pdf.data:
            for archivo in form.archivos_pdf.data:
                if archivo and hasattr(archivo, 'filename') and archivo.filename:
                    filename = secure_filename(archivo.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'concursos', filename)
                    archivo.save(filepath)
                    
                    # Crear registro de archivo
                    archivo_concurso = ArchivoConcurso(
                        concurso_id=concurso.id,
                        nombre_archivo=filename,
                        ruta_archivo=f'uploads/concursos/{filename}',
                        tipo='documento'  # Puedes hacer esto configurable si quieres
                    )
                    db.session.add(archivo_concurso)
        
        db.session.commit()
        flash('Concurso creado correctamente.', 'success')
        return redirect(url_for('admin_concursos'))
    
    return render_template('admin/concurso_form.html', form=form, titulo='Nuevo Concurso')

@app.route('/admin/concursos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_concurso(id):
    concurso = Concurso.query.get_or_404(id)
    form = ConcursoForm(obj=concurso)
    
    # Obtener archivos existentes
    archivos_existentes = ArchivoConcurso.query.filter_by(concurso_id=id).all()
    
    if form.validate_on_submit():
        concurso.titulo = form.titulo.data
        concurso.descripcion = form.descripcion.data
        concurso.fecha = form.fecha.data
        concurso.tipo = form.tipo.data
        concurso.activo = form.activo.data
        
        # Procesar nuevos archivos
        if form.archivos_pdf.data:
            for archivo in form.archivos_pdf.data:
                if archivo and hasattr(archivo, 'filename') and archivo.filename:
                    filename = secure_filename(archivo.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'concursos', filename)
                    archivo.save(filepath)
                    
                    archivo_concurso = ArchivoConcurso(
                        concurso_id=concurso.id,
                        nombre_archivo=filename,
                        ruta_archivo=f'uploads/concursos/{filename}',
                        tipo='documento'
                    )
                    db.session.add(archivo_concurso)
        
        db.session.commit()
        flash('Concurso actualizado correctamente.', 'success')
        return redirect(url_for('admin_concursos'))
    
    return render_template('admin/concurso_form.html', form=form, concurso=concurso, archivos=archivos_existentes, titulo='Editar Concurso')


@app.route('/admin/concursos/eliminar/<int:id>')
@login_required
def eliminar_concurso(id):
    concurso = Concurso.query.get_or_404(id)
    
    # Eliminar archivos asociados
    archivos = ArchivoConcurso.query.filter_by(concurso_id=id).all()
    for archivo in archivos:
        db.session.delete(archivo)
    
    db.session.delete(concurso)
    db.session.commit()
    flash('Concurso y sus archivos eliminados correctamente.', 'success')
    return redirect(url_for('admin_concursos'))

@app.route('/admin/concursos/archivo/eliminar/<int:id>')
@login_required
def eliminar_archivo_concurso(id):
    archivo = ArchivoConcurso.query.get_or_404(id)
    concurso_id = archivo.concurso_id
    db.session.delete(archivo)
    db.session.commit()
    flash('Archivo eliminado correctamente.', 'success')
    return redirect(url_for('editar_concurso', id=concurso_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)