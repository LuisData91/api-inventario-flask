from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


# Cargar las variables de entorno
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = 'LqxYrxsqmVFeQIOKjESbMNGUM2CXXeqC'


# Inicializamos las dependencias
db = SQLAlchemy(app)
jwt = JWTManager(app)


# Modelos
class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    def check_password(self, password):
        bcrypt = Bcrypt(app)
        return bcrypt.check_password_hash(self.password, password)


class Categoria(db.Model):
    __tablename__ = 'Categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)


class Producto(db.Model):
    __tablename__ = 'Productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    precio = db.Column(db.Float, nullable=False, default=0)
    CategoriaId = db.Column(db.Integer, db.ForeignKey('Categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref='Productos')


# Rutas
@app.route('/', methods=['GET'])
def index():
    return "Bienvenido"


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    usuario = Usuario.query.filter_by(email=username).first()
    # Validamos si existe el usuario o la contraseña es incorrecta
    if not usuario or not usuario.check_password(password):
        return({
            'message': 'Credenciales incorrectas'
        })
    # Generamos el token de acceso
    token = create_access_token(identity=str(usuario.email))
    return({
            'token': token
        })


@app.route('/api/categorias', methods=['GET'])
def categorias_listar():
    categorias = Categoria.query.all()
    resultado = [{'id':c.id, 'nombre':c.nombre} for c in categorias]
    return jsonify(resultado)


@app.route('/api/productos', methods=['GET'])
@jwt_required()
def productos_listar():
    productos = Producto.query.all()
    resultado = [{'id':p.id, 'nombre':p.nombre} for p in productos]
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)