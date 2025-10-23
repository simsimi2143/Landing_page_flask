from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import os

db = SQLAlchemy()

class AdminUser(UserMixin):
    def __init__(self, id):
        self.id = id

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(300))
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Noticia {self.titulo}>'

class Alcalde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(300))
    vision = db.Column(db.Text)
    mision = db.Column(db.Text)
    compromisos = db.Column(db.Text)
    logros = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Alcalde {self.nombre}>'

class Concejal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100))
    partido = db.Column(db.String(100))
    comisiones = db.Column(db.Text)  # Guardar como string separado por comas
    biografia = db.Column(db.Text)
    imagen = db.Column(db.String(300))
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Concejal {self.nombre}>'

class Concurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.String(50))
    # Eliminamos archivo_pdf ya que ahora tendrá múltiples archivos
    tipo = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Concurso {self.titulo}>'
    
class ArchivoConcurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id'), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    tipo = db.Column(db.String(50))  # 'bases', 'resultado', 'anexo', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ArchivoConcurso {self.nombre_archivo}>'