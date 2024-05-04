import re
from datetime import datetime
def validar_cpf(numbers):
    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

def validar_cnpj(cnpj):
    cnpj = re.sub("[^0-9]", "", cnpj) 
    if len(cnpj) != 14:
        return False
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for i in range(12):
        soma += int(cnpj[i]) * pesos[i]
    dig1 = soma % 11
    dig1 = 0 if dig1 < 2 else 11 - dig1
    if int(cnpj[12]) != dig1:
        return False
    soma = 0
    pesos.insert(0, 6)
    for i in range(13):
        soma += int(cnpj[i]) * pesos[i]
    dig2 = soma % 11
    dig2 = 0 if dig2 < 2 else 11 - dig2
    if int(cnpj[13]) != dig2:
        return False
    return True

def validar_numero_celular(numero):
    padrao = r"\([0-9]{2}\) 9\s?[0-9]{4}-?[0-9]{4}"
    if re.match(padrao, numero):
        return True
    else:
        return False

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(padrao, email):
        return True
    else:
        return False

def validar_cep(cep):
    padrao_cep = re.compile(r'^\d{5}-?\d{3}$')
    if not padrao_cep.match(cep):
        return False
    return True
def validar_numero(numero):
    if isinstance(numero, int):
        return True
    elif isinstance(numero, str) and numero.isdigit():
        return True
    else:
        return False
def validar_float(numero):
    try:
        float(numero)
        return True
    except ValueError:
        return False
    
def validar_data(data_str):
    try:
        datetime.strptime(data_str, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False
    
