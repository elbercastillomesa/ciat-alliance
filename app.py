from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@db/agronomy'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(correo=email).first()
        if user and user.contraseña == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Crear usuarios, parcelas y actividades
@app.route('/create_user', methods=['POST'])
def create_user():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    rol = request.form['rol']
    new_user = User(nombre=nombre, correo=correo, contraseña=contraseña, rol=rol)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_parcela', methods=['POST'])
def create_parcela():
    latitud = request.form['latitud']
    longitud = request.form['longitud']
    tamaño = request.form['tamaño']
    tipo_cultivo = request.form['tipo_cultivo']
    usuario_id = current_user.id
    new_parcela = Parcela(latitud=latitud, longitud=longitud, tamaño=tamaño, tipo_cultivo=tipo_cultivo, usuario_id=usuario_id)
    db.session.add(new_parcela)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_actividad', methods=['POST'])
def create_actividad():
    fecha = request.form['fecha']
    tipo_actividad = request.form['tipo_actividad']
    insumos_utilizados = request.form['insumos_utilizados']
    duracion = request.form['duracion']
    parcela_id = request.form['parcela_id']
    usuario_id = current_user.id
    new_actividad = Actividad(fecha=fecha, tipo_actividad=tipo_actividad, insumos_utilizados=insumos_utilizados, duracion=duracion, parcela_id=parcela_id, usuario_id=usuario_id)
    db.session.add(new_actividad)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()        
    app.run(host='0.0.0.0', debug=True)
