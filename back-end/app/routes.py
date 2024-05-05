from app.functions import validar_cnpj,validar_cpf,validar_email,validar_numero_celular,validar_cep,validar_numero,validar_float,validar_data
from flask import request, jsonify
from . import app, db
from .model import Customer, Address, Item, Pedido, Pedido_Item

#Cliente
@app.route('/cliente/cadastro',methods=['POST'])
def CustomerRegistration():
    data = request.get_json()
    name = data.get("name")
    lastname = data.get("lastname")
    cpf = data.get("cpf")
    cnpj = data.get("cnpj")
    email = data.get("email")
    phone1 = data.get("phone1")
    phone2 = data.get("phone2")
    
    #Validação dados
    if(cpf != '' and validar_cpf(cpf)==False):
        return jsonify({'message': 'Cpf em formato invalido'}), 401
    if(cnpj != '' and validar_cnpj(cnpj)==False):
        return jsonify({'message': 'Cnpj em formato invalido'}), 401
    if(cpf == '' and cnpj == ''):
        return jsonify({'message': 'Precisa informar ao menos o cpf ou um cnpj'}), 401
    if(cpf==''):
        cpf = None
    if(cnpj==''):
        cnpj = None
    if(email == '' or validar_email(email)==False):
        return jsonify({'message': 'Email nulo ou em fromato invalido'}), 401
    if(phone1 != '' and validar_numero_celular(phone1)==False):
        return jsonify({'message': 'Telefone 1 em formato invalido'}), 401
    if(phone2 != '' and validar_numero_celular(phone2)==False):
        return jsonify({'message': 'Telefone 2 em formato invalido'}), 401
    if(phone1==''and phone2 == ''):
        return jsonify({'message': 'Precisa informar ao menos um número'}), 401
    if(name == '' or len(name)>100):
        return jsonify({'message': 'Nome nulo ou maior que 100 caracteres'}), 401
    if(lastname == '' or len(lastname)>100):
        return jsonify({'message': 'Sobrenome nulo ou maior que 100 caracteres'}), 401
    try:
        customer = Customer(name=name,lastname=lastname,cpf=cpf,cnpj=cnpj,email=email,phone1=phone1,phone2=phone2)        
        db.session.add(customer)
        db.session.commit()
        return jsonify({"success": True, "user_id": customer.id}), 201 
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': f'Houve um erro ao tentar adicionar no banco de dados:{str(e)}'}), 401
    
    
@app.route('/cliente/lista',methods=["GET"])
def AllCustomerList():
    customers = Customer.query.all()
    dic_list = []
    for customer in customers:
        dic = {
       "id": customer.id,
        "name": customer.name,
        "lastname":customer.lastname,
        "cpf":customer.cpf,
        "cnpj":customer.cnpj,
        "email":customer.email,
        "phone1":customer.phone1,
        "phone2":customer.phone2}
        dic_list.append(dic)
    return jsonify(dic_list)

@app.route('/cliente/<string:cpf>',methods=["GET"])
def GetCustumerByCpf(cpf):
    customer = Customer.query.filter_by(cpf=cpf).first()
    dic = {
       "id": customer.id,
        "name": customer.name,
        "lastname":customer.lastname,
        "cpf":customer.cpf,
        "cnpj":customer.cnpj,
        "email":customer.email,
        "phone1":customer.phone1,
        "phone2":customer.phone2}
    return jsonify(dic)

@app.route('/cliente/<int:id>',methods=["GET"])
def GetCustomerById(id):
    customer = Customer.query.filter_by(id=id).first()
    dic = {
       "id": customer.id,
        "name": customer.name,
        "lastname":customer.lastname,
        "cpf":customer.cpf,
        "cnpj":customer.cnpj,
        "email":customer.email,
        "phone1":customer.phone1,
        "phone2":customer.phone2}
    return jsonify(dic)

@app.route('/cliente/email/<string:email>',methods=["GET"])
def GetCustomerByEmail(email):
    customer = Customer.query.filter_by(email=email).first()
    dic = {
       "id": customer.id,
        "name": customer.name,
        "lastname":customer.lastname,
        "cpf":customer.cpf,
        "cnpj":customer.cnpj,
        "email":customer.email,
        "phone1":customer.phone1,
        "phone2":customer.phone2}
    return jsonify(dic)

@app.route('/cliente/<int:id>',methods=["DELETE"])
def DeleteCustomer(id):
    try:
        customer = Customer.query.filter_by(id=id).first()
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': "Deletado com sucesso"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Houve um erro ao tentar remover elemento do banco dados:{str(e)}'}), 401

#--------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- --------------------------------  
    
#Endereço    
@app.route('/endereco/cadastro',methods=['POST'])
def AddresRegistration():
    data = request.get_json()
    cidade = data.get("cidade")
    estado = data.get("estado")
    rua = data.get("rua")
    numero = data.get("numero")
    quadra = data.get("quadra")
    lote = data.get("lote")
    cep = data.get("cep")
    descricao = data.get("descricao")
    referencia = data.get("referencia")
    cliente_id = data.get("cliente_id")
    #Validação dados
    if(cep == '' or validar_cep(cep)==False):
        return jsonify({'message': 'CEP em formato invalido'}), 401
    if(rua == '' or len(rua)>100):
        return jsonify({'message': 'Rua nula ou maior que 100 caracteres'}), 401
    if(cidade == '' or len(cidade)>100):
        return jsonify({'message': 'Cidade nula ou maior que 100 caracteres'}), 401
    if(estado == '' or len(estado)>100):
        return jsonify({'message': 'Estado nulo ou maior que 100 caracteres'}), 401
    if(numero == '' or validar_numero(numero)==False):
        return jsonify({'message': 'Numero nulo ou em formato invalido'}), 401
    if(quadra == '' or validar_numero(quadra)==False):
        return jsonify({'message': 'Quadra nula ou em formato invalido'}), 401
    if(lote == '' or validar_numero(lote)==False):
        return jsonify({'message': 'Lote em formato invalido'}), 401
    if(len(descricao) > 100):
        return jsonify({'message': 'decrição maior que 100 caracteres'}), 401
    if(len(referencia)>100):
        return jsonify({'message': 'referencia maior que 100 caracteres'}), 401
    if(cliente_id == ''):
        return jsonify({'message': 'id de cliente nulo'}), 401
    try:
        address = Address(rua=rua,cidade=cidade,estado=estado,numero=numero,quadra=quadra,lote=lote,descricao=descricao,referencia=referencia,cep=cep,cliente_id=cliente_id)
        db.session.add(address)
        db.session.commit()
        return jsonify({"success": True, "id": address.id,"mensagem":"Endereço criado com sucesso"}), 201 
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': f'Houve um erro ao tentar adicionar no banco de dados:{str(e)}'}), 401

@app.route('/endereco/lista',methods=["GET"])
def GetAllAddress():  
    addresses = Address.query.all()
    dic_list = []
    for address in addresses:
        customer = Customer.query.filter_by(id=address.cliente_id).first()
        dic_customer = {
        "id": customer.id,
        "name": customer.name,
        "lastname":customer.lastname,
        "cpf":customer.cpf,
        "cnpj":customer.cnpj,
        "email":customer.email,
        "phone1":customer.phone1,
        "phone2":customer.phone2} 
        dic_endereco = {
        "id_cidade":address.id,
        "cidade" : address.cidade,
        "estado" : address.estado,
        "rua" : address.rua,
        "numero": address.numero,
        "quadra" : address.quadra,
        "lote" : address.lote,
        "cep" : address.cep,
        "descricao" :address.descricao,
        "referencia" : address.referencia,
        "cliente" : dic_customer}
        dic_list.append(dic_endereco)
    return jsonify(dic_list)

@app.route('/endereco/<int:id>',methods=["GET"])
def GetAddressById(id):  
    address = Address.query.filter_by(id=id).first()
    customer = Customer.query.filter_by(id=address.cliente_id).first()
    dic_customer = {
    "id": customer.id,
    "name": customer.name,
    "lastname":customer.lastname,
    "cpf":customer.cpf,
    "cnpj":customer.cnpj,
    "email":customer.email,
    "phone1":customer.phone1,
    "phone2":customer.phone2} 
    dic_endereco = {
    "id_cidade":address.id,
    "cidade" : address.cidade,
    "estado" : address.estado,
    "rua" : address.rua,
    "numero": address.numero,
    "quadra" : address.quadra,
    "lote" : address.lote,
    "cep" : address.cep,
    "descricao" :address.descricao,
    "referencia" : address.referencia,
    "cliente" : dic_customer}
    return jsonify(dic_endereco)

@app.route('/endereco/cliente/<int:id>',methods=["GET"])
def GetAddressByClienteId(id):  
    address = Address.query.filter_by(cliente_id=id).first()
    customer = Customer.query.filter_by(id=id).first()
    dic_customer = {
    "id": customer.id,
    "name": customer.name,
    "lastname":customer.lastname,
    "cpf":customer.cpf,
    "cnpj":customer.cnpj,
    "email":customer.email,
    "phone1":customer.phone1,
    "phone2":customer.phone2} 
    dic_endereco = {
    "id_cidade":address.id,
    "cidade" : address.cidade,
    "estado" : address.estado,
    "rua" : address.rua,
    "numero": address.numero,
    "quadra" : address.quadra,
    "lote" : address.lote,
    "cep" : address.cep,
    "descricao" :address.descricao,
    "referencia" : address.referencia,
    "cliente" : dic_customer}
    return jsonify(dic_endereco)


@app.route('/endereco/<int:id>',methods=["DELETE"])
def DeleteAddress(id):
    try:
        address = Address.query.filter_by(id=id).first()
        db.session.delete(address)
        db.session.commit()
        return jsonify({'message': "Deletado com sucesso"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Houve um erro ao tentar remover elemento do banco dados:{str(e)}'}), 401

    
  #--------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- --------------------------------  

#item
@app.route('/item/cadastro',methods=['POST'])
def ItemRegistration():
    data = request.get_json()
    nome = data.get("nome")
    preco = data.get("preco")
    descricao = data.get("descricao")
    codigo = data.get("codigo")
  
    #Validação dados
    if(nome == '' or len(nome)>100):
        return jsonify({'message': 'Nome nulo ou maior que 100 caracteres'}), 401
    if(preco == '' or validar_float(preco)==False):
        return jsonify({'message': 'Preco numero ou em formato invalido'}), 401
    if(len(descricao)>100):
        return jsonify({'message': 'Descrição maior que 100 caracteres'}), 401
    if(codigo == '' or len(codigo)>100):
        return jsonify({'message': 'Codigo nulo ou maior que 100 caracteres'}), 401
 
    try:
        item = Item(nome=nome, preco=preco,descricao=descricao,codigo=codigo)
        db.session.add(item)
        db.session.commit()
        return jsonify({"success": True, "id": item.id,"mensagem":"Endereço criado com sucesso"}), 201 
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': f'Houve um erro ao tentar adicionar no banco de dados:{str(e)}'}), 401
    
    
@app.route('/item/lista',methods=["GET"])
def GetAllItens():  
    itens = Item.query.all()
    dic_list = []
    for item in itens:
        dic_item = {
        "nome":item.nome,
        "preco": item.preco,
        "descricao": item.descricao,
        "codigo" :item.codigo} 
        dic_list.append(dic_item)
    return jsonify(dic_list)

@app.route('/item/<int:id>',methods=["GET"])
def GetItemById(id):  
    item = Item.query.filter_by(id=id).first()
    dic_item = {
    "nome":item.nome,
    "preco": item.preco,
    "descricao": item.descricao,
    "codigo" :item.codigo} 
    return jsonify(dic_item)

@app.route('/item/codigo/<string:code>',methods=["GET"])
def GetItemByCode(code):  
    item = Item.query.filter_by(codigo=code).first()
    dic_item = {
    "nome":item.nome,
    "preco": item.preco,
    "descricao": item.descricao,
    "codigo" :item.codigo} 
    return jsonify(dic_item)

@app.route('/item/<int:id>',methods=["DELETE"])
def DeleteItem(id):
    try:
        item = Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': "Deletado com sucesso"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Houve um erro ao tentar remover elemento do banco dados:{str(e)}'}), 401
        
        
  #--------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- --------------------------------  

#Pedido        
@app.route('/pedido/cadastro',methods=['POST'])
def PedidoRegistration():
    data = request.get_json()
    lista_itens = data.get("lista_itens")
    data_entrega = data.get("data_entrega")
    descricao = data.get("descricao")
    cliente_id = data.get("cliente_id")
    endereco_id = data.get("endereco_id")
   
  
    #Validação dados
    if(len(descricao)>100):
        return jsonify({'message': 'Nome nulo ou maior que 100 caracteres'}), 401
    if(cliente_id == '' or validar_numero(cliente_id)== False):
        return jsonify({'message': 'id de cliente nulo ou diferente do formato'}), 401
    if(endereco_id == '' or validar_numero(endereco_id)== False):
        return jsonify({'message': 'id do endereço nulo ou diferente do formato'}), 401
    if(data_entrega == '' or validar_data(data_entrega)== False):
        return jsonify({'message': 'Data nula ou diferente do formato dd/mm/YYYY HH:MM'}), 401
    preco_final = 0.0
    
    for i in lista_itens:
        item = Item.query.get(i["id_item"])
        preco_final += item.preco * i["quantidade_item"]

    try:
        pedido = Pedido(data=data_entrega,cliente_id=cliente_id,endereco_id=endereco_id,descricao=descricao,preco_final=preco_final)
        db.session.add(pedido)
        db.session.commit()
        for i in lista_itens:
            pedido_item = Pedido_Item(pedido_id=pedido.id,item_id = i["id_item"],quantidade = i["quantidade_item"])
            db.session.add(pedido_item)
            db.session.commit()
        return jsonify({"success": True, "id": pedido.id,"mensagem":"Endereço criado com sucesso"}), 201 
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': f'Houve um erro ao tentar adicionar no banco de dados:{str(e)}'}), 401
        
  #--------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- -------------------------------- --------------------------------  
       
    