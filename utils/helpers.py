from datetime import datetime, date

def formatar_data(data, formato="%d/%m/%Y"):
    if not data:
        return ""
    if isinstance(data, str):
        data = datetime.strptime(data, "%Y-%m-%d")
    return data.strftime(formato)

def calcular_idade(data_nasc):
    if not data_nasc:
        return 0
    if isinstance(data_nasc, str):
        data_nasc = datetime.strptime(data_nasc, "%Y-%m-%d").date()
    hoje = date.today()
    idade = hoje.year - data_nasc.year
    if hoje.month < data_nasc.month or (hoje.month == data_nasc.month and hoje.day < data_nasc.day):
        idade -= 1
    return idade