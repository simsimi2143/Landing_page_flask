import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'clave-secreta-temporal-cambiar-en-produccion'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'municipalidad.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Extensiones permitidas para imágenes
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configuración del panel admin
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS