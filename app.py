from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


# Cargar las variables de entorno
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Inicializamos la base de datos
db = SQLAlchemy(app)


# Modelos
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


@app.route('/api/categorias', methods=['GET'])
def categorias_listar():
    categorias = Categoria.query.all()
    resultado = [{'id':c.id, 'nombre':c.nombre} for c in categorias]
    return jsonify(resultado)


@app.route('/api/productos', methods=['GET'])
def productos_listar():
    productos = Producto.query.all()
    resultado = [{'id':p.id, 'nombre':p.nombre, 'categoria':p.categoria.nombre} for p in productos]
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)