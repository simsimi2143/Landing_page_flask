from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, DateField, SelectField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = StringField('Contraseña', validators=[DataRequired()])

class NoticiaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    contenido = TextAreaField('Contenido', validators=[DataRequired()])
    imagen = FileField('Imagen', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes!')])
    activa = BooleanField('Activa')

class AlcaldeForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    imagen = FileField('Imagen', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes!')])
    vision = TextAreaField('Visión')
    mision = TextAreaField('Misión')
    compromisos = TextAreaField('Compromisos')
    logros = TextAreaField('Logros')

class ConcejalForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cargo = StringField('Cargo')
    partido = StringField('Partido')
    comisiones = TextAreaField('Comisiones (separar por comas)')
    biografia = TextAreaField('Biografía')
    imagen = FileField('Imagen', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes!')])
    activo = BooleanField('Activo', default=True)
    orden = IntegerField('Orden', default=0)

class ConcursoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    fecha = StringField('Fecha')
    # Cambiamos a MultipleFileField para permitir varios archivos
    archivos_pdf = MultipleFileField('Archivos PDF', validators=[Optional(), FileAllowed(['pdf'], 'Solo archivos PDF!')])
    tipo = SelectField('Tipo', choices=[
        ('convocatoria', 'Convocatoria'),
        ('resultado', 'Resultado'),
        ('decreto', 'Decreto')
    ])
    activo = BooleanField('Activo', default=True)