from . import db  # Importa a instância de SQLAlchemy do pacote

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(100), unique=True)
    cnpj = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone1 = db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    quadra = db.Column(db.Integer,nullable=False)
    lote = db.Column(db.Integer, nullable=False)
    cep = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100))
    referencia = db.Column(db.String(100))
    cliente_id = db.Column(db.Integer, primary_key=True,nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100))
    preco = db.Column(db.Float, nullable=False)
    codigo = db.Column(db.String(100), nullable=False,unique = True)
