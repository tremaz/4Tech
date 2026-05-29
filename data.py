# Tratamento dos dados das planilhas - Gupy e SupplyGo
import pandas as pd
from typing import Optional

# Carregamento dos dados
DataGupy = pd.read_excel("./Participants-36809.xlsx", index_col=None, keep_default_na=False, na_values='nan')
DataSupplyGo = pd.read_excel("./Relatório SupplyGo - Desafio_Hack-ta-on.xlsx", header=6, index_col=None, keep_default_na=False, na_values='nan', sheet_name="Relatorio")

# Mapa de normalização de estados
ESTADOS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima",
    "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}

ESTADOS_NOME = {
    "ACRE": "AC", "ALAGOAS": "AL", "AMAPA": "AP", "AMAZONAS": "AM",
    "BAHIA": "BA", "CEARA": "CE", "CEARA": "CE", "DISTRITO FEDERAL": "DF",
    "ESPIRITO SANTO": "ES", "ESPIRITO SANTO": "ES", "GOIAS": "GO", "GOIAS": "GO",
    "MARANHAO": "MA", "MATO GROSSO": "MT", "MATO GROSSO DO SUL": "MS",
    "MINAS GERAIS": "MG", "PARA": "PA", "PARAIBA": "PB", "PARANA": "PR",
    "PERNAMBUCO": "PE", "PIAUI": "PI", "RIO DE JANEIRO": "RJ",
    "RIO GRANDE DO NORTE": "RN", "RIO GRANDE DO SUL": "RS",
    "RONDONIA": "RO", "RORAIMA": "RR", "SANTA CATARINA": "SC",
    "SAO PAULO": "SP", "SERGIPE": "SE", "TOCANTINS": "TO",
}


def UFES(valor):
    """Retorna o nome completo da UF dado o código ou nome."""
    valor = str(valor).strip()
    if len(valor) == 2:
        return ESTADOS.get(valor.upper(), "UF inválida")
    invertido = {v: k for k, v in ESTADOS.items()}
    return invertido.get(valor.lower(), "Estado inválido")


def selectEstadoG():
    """Seleciona estado para filtro Gupy (interativo)."""
    global quantEstado, EstadoDesejado
    quantEstado = 0
    EstadoDesejado = input("Digite o UF do estado desejado: ")
    for i in range(len(DataGupy)):
        if DataGupy.iloc[i]["Estado"] == EstadoDesejado:
            quantEstado += 1
    return EstadoDesejado


def taxaDeConclusaoG():
    """Calcula taxa de conclusão para estado selecionado no Gupy."""
    taxa = 0
    for i in range(len(DataGupy)):
        if DataGupy.iloc[i]["Estado"] == EstadoDesejado and DataGupy.iloc[i]["Status de realização"] == "Concluído":
            taxa += 1
    calculo = round((taxa / quantEstado) * 100, 2) if quantEstado else 0
    print(f"{calculo}% é a taxa de conclusão do estado {EstadoDesejado}")
    return calculo


def iniciadosG():
    """Lista quem iniciou o treinamento no estado selecionado (Gupy)."""
    print(f"No estado {EstadoDesejado} iniciaram: ")
    for i in range(len(DataGupy)):
        if (DataGupy.iloc[i]["Data de início na trilha"] != "" and
                DataGupy.iloc[i]["Data de finalização na trilha"] != "" and
                DataGupy.iloc[i]["Estado"] == EstadoDesejado):
            print(i, DataGupy.iloc[i]["Chefia ADP"])


def naoIniciadosG():
    """Lista quem não iniciou o treinamento no estado selecionado (Gupy)."""
    print(f"No estado {EstadoDesejado} não iniciaram: ")
    for i in range(len(DataGupy)):
        if (DataGupy.iloc[i]["Data de início na trilha"] == "" and
                DataGupy.iloc[i]["Data de finalização na trilha"] == "" and
                DataGupy.iloc[i]["Estado"] == EstadoDesejado):
            print(i, DataGupy.iloc[i]["Chefia ADP"])


def concluidosG():
    """Lista quem concluiu o curso no estado selecionado (Gupy)."""
    print(f"Concluidos no estado {EstadoDesejado}: ")
    for i in range(len(DataGupy)):
        if DataGupy.iloc[i]["Status de realização"] == "Concluído" and DataGupy.iloc[i]["Estado"] == EstadoDesejado:
            print(i, DataGupy.iloc[i]["Chefia ADP"])


def concluidoTotG():
    """Retorna quantidade total de concluídos no Gupy."""
    return int((DataGupy["Status de realização"] == "Concluído").sum())


def quantG():
    """Retorna quantidade total de registros no Gupy."""
    return len(DataGupy)


# ===== PARTE SUPPLY GO =====

def selectEstadoS():
    """Seleciona estado para filtro SupplyGo (interativo)."""
    global EstadoDesejado, quantEstado
    quantEstado = 0
    EstadoDesejado = input("Digite o nome do estado desejado: ").upper()
    for i in range(len(DataSupplyGo)):
        if DataSupplyGo.iloc[i]["ESTADO"] == EstadoDesejado:
            quantEstado += 1
    return EstadoDesejado


def taxaDeConclusaoS():
    """Calcula taxa de conclusão geral da SupplyGo."""
    taxa = int((DataSupplyGo["Status Trilha"] == "Concluído").sum())
    calculo = round((taxa / len(DataSupplyGo)) * 100, 2) if len(DataSupplyGo) else 0
    print(f"{calculo}% é a taxa de conclusão geral da SupplyGo")
    return calculo


def concluidosS():
    """Retorna quantidade de concluídos no estado selecionado (SupplyGo)."""
    count = 0
    for i in range(len(DataSupplyGo)):
        if (DataSupplyGo.iloc[i]["Carga Horária Total"] == DataSupplyGo.iloc[i]["Carga Horária Cursada"] and
                DataSupplyGo.iloc[i]["ESTADO"] == EstadoDesejado):
            count += 1
    print(f"{count} concluídos no estado {EstadoDesejado}")
    return count


def concluindoS():
    """Retorna quantidade de cursando no estado selecionado (SupplyGo)."""
    count = 0
    for i in range(len(DataSupplyGo)):
        if (DataSupplyGo.iloc[i]["Carga Horária Total"] != DataSupplyGo.iloc[i]["Carga Horária Cursada"] and
                DataSupplyGo.iloc[i]["ESTADO"] == EstadoDesejado):
            count += 1
    return count


def concluidoTotS():
    """Retorna quantidade total de concluídos na SupplyGo."""
    return int((DataSupplyGo["Status Trilha"] == "Concluído").sum())


def quantS():
    """Retorna quantidade total de registros na SupplyGo."""
    return len(DataSupplyGo)


def concluidosTot():
    """Retorna total combinado de concluídos (Gupy + SupplyGo)."""
    quantCursando = quantG() + quantS()
    quantConcluido = concluidoTotG() + concluidoTotS()
    print(f"Foram analisados {quantCursando} colaboradores, dos quais {quantConcluido} concluíram")
    return round(quantConcluido / quantCursando * 100, 2) if quantCursando else 0
