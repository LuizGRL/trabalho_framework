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