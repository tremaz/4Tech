#tratamento dos dados das planilhas
import numpy as np
import pandas as pd

DataGupy = pd.read_excel(".\Participants-36809.xlsx", index_col=None, keep_default_na=False , na_values= 'nan') #AQUI DADOS DA GUPY
DataSuplyGo = pd.read_excel(".\Relatório SupplyGo - Desafio_Hack-ta-on.xlsx",header=6, index_col=None, keep_default_na=False , na_values= 'nan', sheet_name="Relatorio") #AQUI DADOS SUPPLyGO

# PARTE GUPY

def selectEstado():
    global quantEstado
    global EstadoDesejado
    quantEstado = 0
    EstadoDesejado = input("Digite o UF do estado desejado: ")
    for i in range(len(DataGupy)):
        if DataGupy.iloc[i]["Estado"] == EstadoDesejado:
            quantEstado = quantEstado+1

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

    # print(ConcluidosDoEstado)

# PARTE SUPPLY GO

def taxaDeConclusãoS():
    taxa = 0
    for i in range(len(DataSuplyGo)):
        info = DataSuplyGo.iloc[i]["Status Trilha"]
        if(info == "Concluído"):
            taxa = taxa + 1
    calculoTaxa = round((taxa/(len(DataSuplyGo)))*100, 2)
    print(f"{calculoTaxa} % é a taxa de conclusão geral da SupplyGo")
    return calculoTaxa

def concluidosS():
    for i in range(len(DataSuplyGo)):
        dataTot = DataSuplyGo.iloc[i]["Carga Horária Total"]
        dataCurs = DataSuplyGo.iloc[i]["Carga Horária Cursada"]
        if dataTot == dataCurs:
            print(i, DataSuplyGo.iloc[i]["Nome"])

def inConcS(): 
    for i in range(len(DataSuplyGo)):
        dataTot = DataSuplyGo.iloc[i]["Carga Horária Total"]
        dataCurs = DataSuplyGo.iloc[i]["Carga Horária Cursada"]
        if dataTot != dataCurs:
            print(i, DataSuplyGo.iloc[i]["Nome"])

#Pseudo Menu

def run():
    objetivo = 0
    while objetivo != 5:
        objetivo = int(input(f"0 - Mudar estado || 1 - Taxa de conclusão || 2 - Iniciados || 3 - Não Iniciados || 4 - Concluidos || 5 - Sair\n"))
        match objetivo:
            case 0: print(f"Estado: {EstadoDesejado}"), selectEstado()

            case 1: taxaDeConclusãoG()

            case 2: iniciadosG()

            case 3: naoIniciadosG()

            case 4: concluidosG()      

selectEstado()
run()
print(quantEstado)