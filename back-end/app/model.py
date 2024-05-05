from . import db  
from sqlalchemy.orm import relationship

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
    children = relationship("Pedido_Item", cascade="all, delete", backref="parent")



class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    data = db.Column(db.Date, nullable=False)
    preco_final = db.Column(db.Float, nullable=False)
    cliente_id =   db.Column(db.Integer, nullable= False)
    endereco_id =  db.Column(db.Integer, nullable= False)
    descricao = db.Column(db.String(100))
    children = relationship("Pedido_Item", cascade="all, delete", backref="pedido")


class Pedido_Item(db.Model):
    __tablename__ = 'pedido_item'
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'),primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)

