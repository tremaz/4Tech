#tratamento dos dados das planilhas
import numpy as np
import pandas as pd

DataGupy = pd.read_excel("./Participants-36809.xlsx", index_col=None, keep_default_na=False , na_values= 'nan') #AQUI DADOS DA GUPY
DataSuplyGo = pd.read_excel("./Relatório SupplyGo - Desafio_Hack-ta-on.xlsx",header=6, index_col=None, keep_default_na=False , na_values= 'nan', sheet_name="Relatorio") #AQUI DADOS SUPPLyGO

# PARTE GUPY

def estado_ou_uf(valor):
    estados = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins"
    }

    valor = valor.strip()

    # Se for UF
    if len(valor) == 2:
        return estados.get(valor.upper(), "UF inválida")

    # Se for nome do estado
    estados_invertido = {v.lower(): k for k, v in estados.items()}
    return estados_invertido.get(valor.lower(), "Estado inválido")

def selectEstadoG():
    global quantEstado
    global EstadoDesejado
    quantEstado = 0
    EstadoDesejado = input("Digite o UF do estado desejado: ")
    for i in range(len(DataGupy)):
        if DataGupy.iloc[i]["Estado"] == EstadoDesejado:
            quantEstado = quantEstado+1
    return EstadoDesejado

def taxaDeConclusãoG():
    taxa = 0
    for i in range(len(DataGupy)):
        dataEs = DataGupy.iloc[i]["Estado"]
        info = DataGupy.iloc[i]["Status de realização"]
        if (info == "Concluído") and (dataEs == EstadoDesejado):
            taxa = taxa + 1
    calculoTaxa = round((taxa/quantEstado)*100, 2)
    print(f"{calculoTaxa} % é a taxa de conclusão do estado {EstadoDesejado}")
    return calculoTaxa

def iniciadosG():
    print(f"No estado {EstadoDesejado} iniciaram: ")
    for i in range(len(DataGupy)):
        dataEs = DataGupy.iloc[i]["Estado"]
        dataIn = DataGupy.iloc[i]["Data de início na trilha"]
        dataFi = DataGupy.iloc[i]["Data de finalização na trilha"]
        if (dataIn != "") and (dataFi != "") and (dataEs == EstadoDesejado):
            print(i, DataGupy.iloc[i]["Chefia ADP"])

def naoIniciadosG():
    print(f"No estado {EstadoDesejado} não iniciaram: ")
    for i in range(len(DataGupy)):
        dataEs = DataGupy.iloc[i]["Estado"]
        dataIn = DataGupy.iloc[i]["Data de início na trilha"]
        dataFi = DataGupy.iloc[i]["Data de finalização na trilha"]
        if (dataIn == "") and (dataFi == "") and (dataEs == EstadoDesejado):
            print(i, DataGupy.iloc[i]["Chefia ADP"])


def concluidosG(): #Mostra quem concluiu o curso em um estado selecionado
    print(f"Concluidos no estado {EstadoDesejado}: ")
    for i in range(len(DataGupy)):
        dataEs = DataGupy.iloc[i]["Estado"]
        dataIn = DataGupy.iloc[i]["Status de realização"]
        if (dataIn == "Concluído") and (dataEs == EstadoDesejado):
            print(i, DataGupy.iloc[i]["Chefia ADP"])

def concluidoG(Sla): #Mostra quantos concluiram o curso
    # print(f"Concluidos no estado {EstadoDesejado}: ")
    count = 0
    for i in range(len(DataGupy)):
        dataEs = DataGupy.iloc[i]["Estado"]
        dataIn = DataGupy.iloc[i]["Status de realização"]
        if (dataIn == "Concluído"):
            # print(i, DataGupy.iloc[i]["Chefia ADP"])
            count = count + 1
    return count
    
def quantG():
    count = 0
    for i in range(len(DataGupy)):
        count = count + 1
    return count

# PARTE SUPPLY GO

def selectEstadoS():
    global EstadoDesejado
    global quantEstado
    quantEstado = 0
    EstadoDesejado = input("Digite o nome do estado desejado: ").upper()
    for i in range(len(DataSuplyGo)):
        if DataSuplyGo.iloc[i]["ESTADO"] == EstadoDesejado:
            quantEstado = quantEstado+1
    return EstadoDesejado

def taxaDeConclusãoS():
    taxa = 0
    for i in range(len(DataSuplyGo)):
        info = DataSuplyGo.iloc[i]["Status Trilha"]
        if(info == "Concluído"):
            taxa = taxa + 1
    calculoTaxa = round((taxa/quantEstado)*100, 2)
    print(f"{calculoTaxa} % é a taxa de conclusão geral da SupplyGo")
    return calculoTaxa

def concluidosS(): #Mostra quantos concluiram o curso no estado e RETORNA A QUANTIDADE
    for i in range(len(DataSuplyGo)):
        count = 0
        dataTot = DataSuplyGo.iloc[i]["Carga Horária Total"]
        dataCurs = DataSuplyGo.iloc[i]["Carga Horária Cursada"]
        dataEs = DataSuplyGo.iloc[i]["ESTADO"]
        if dataTot == dataCurs and dataEs == EstadoDesejado:
            print(i, DataSuplyGo.iloc[i]["Nome"], f" concluiram no estado {EstadoDesejado}")
            count = count + 1            
    return count
def concluindoS(): 
    count = 0
    for i in range(len(DataSuplyGo)):
        dataEs = DataSuplyGo.iloc[i]["ESTADO"]
        dataTot = DataSuplyGo.iloc[i]["Carga Horária Total"]
        dataCurs = DataSuplyGo.iloc[i]["Carga Horária Cursada"]
        if dataTot != dataCurs and dataEs == EstadoDesejado and dataEs == EstadoDesejado:
            print(i, DataSuplyGo.iloc[i]["Nome"])
            count = count + 1
    return count  

def concluidoS(Sla): #Conta todos que concluiram o curso na S e RETORNA A QUANTIDADE
    for i in range(len(DataSuplyGo)):
        count = 0
        dataTot = DataSuplyGo.iloc[i]["Carga Horária Total"]
        dataCurs = DataSuplyGo.iloc[i]["Carga Horária Cursada"]
        if dataTot == dataCurs:
            # print(i, DataSuplyGo.iloc[i]["Nome"])
            count = count + 1            
    return count
            
def quantS():
    count = 0
    for i in range(len(DataSuplyGo)):
        count = count + 1
    return count


def concluidosTot():
    print(f"Foram analisados {quantG() + quantG()} colaboradores, dos quais, {concluidoG(1) + concluidoS(1)}, concluiram")

#Pseudo Menu

def run():
    selectEstadoS()
    objetivo = 0
    while objetivo != 9:
        objetivo = int(input(f"0 - Mudar estado || 1 - Taxa de conclusão || 2 - Iniciados || 3 - Não Iniciados || 4 - Concluidos || 9 - Sair\n"))
        match objetivo:
            case 0: print(f"Estado: {EstadoDesejado}"), selectEstadoG()

            case 1: taxaDeConclusãoG()

            case 2: iniciadosG()

            case 3: naoIniciadosG()

            case 4: concluidosG()

            case 5: taxaDeConclusãoS()

            case 6: concluindoS()

            case 7: concluidosS()

selectEstadoG()
concluidosTot()
