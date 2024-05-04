import re
def validar_cpf(cpf):
    cpf = re.sub("[^0-9]", "", cpf) 
    if len(cpf) != 11:
        return False    
    cpf_calc = cpf[:9]
    for i in range(9, 11):
        v = sum((i+1)*int(c) for i, c in enumerate(cpf_calc)) % 11
        if v > 9:
            v = 0
        if str(v) != cpf[i]:
            return False
        cpf_calc += cpf[i]
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