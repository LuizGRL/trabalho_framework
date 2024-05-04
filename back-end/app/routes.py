from app.functions import validar_cnpj,validar_cpf,validar_email,validar_numero_celular
from flask import request, jsonify
from . import app, db
import pandas as pd    
from .model import Customer
# DATABASE_URL = "postgresql://postgres:123@localhost/framework"
# engine = create_engine(DATABASE_URL)

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
        df = pd.DataFrame([request.get_json()])
        
        db.session.add(customer)
        db.session.commit()
        return jsonify({"success": True, "user_id": customer.id}), 201

        # with engine.connect() as connection:
        #     # sql_string = text(f"""INSERT INTO customer (name, lastname, cpf, cnpj, email, phone1, phone2) VALUES
        #     #             ('{name}', '{lastname}', '{cpf}', '{cnpj}','{email}','{phone1}','{phone2}');""")
        #     # result = connection.execute(sql_string)
        #     connection.execute(df.to_sql("customer",engine,if_exists="append"))
        #     connection.commit()
        #     connection.close()
        # return jsonify({'message': 'Cliente adicionado com sucesso!'}), 200      
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': f'Houve um erro ao tentar adicionar no banco de dados:{str(e)}'}), 401
        
    