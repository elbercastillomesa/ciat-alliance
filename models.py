from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(10), nullable=False)

class Parcela(db.Model):
    __tablename__ = 'parcelas'
    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Numeric(9, 6), nullable=False)
    longitud = db.Column(db.Numeric(9, 6), nullable=False)
    tamaño = db.Column(db.Numeric(10, 2), nullable=False)
    tipo_cultivo = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class Actividad(db.Model):
    __tablename__ = 'actividades'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    tipo_actividad = db.Column(db.String(255), nullable=False)
    insumos_utilizados = db.Column(db.Text)
    duracion = db.Column(db.Integer, nullable=False)
    parcela_id = db.Column(db.Integer, db.ForeignKey('parcelas.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))    