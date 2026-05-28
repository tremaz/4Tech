#tratamento dos dados das planilhas
import numpy as np
import pandas as pd

DataGupy = pd.read_excel(".\Participants-36809.xlsx", index_col=None, keep_default_na=False , na_values= 'nan') #AQUI DADOS DA GUPY
DataSuplyGo = pd.read_excel(".\Relatório SupplyGo - Desafio_Hack-ta-on.xlsx",header=6, index_col=None, keep_default_na=False , na_values= 'nan', sheet_name="Relatorio") #AQUI DADOS SUPPLyGO

# PARTE GUPY

def taxaDeConclusãoG():
    taxa = 0
    for i in range(len(DataGupy)):
        info = DataGupy.iloc[i]["Status de realização"]
        if(info == "Concluído"):
            taxa = taxa + 1
    calculoTaxa = round((taxa/(len(DataGupy)))*100, 2)
    print(calculoTaxa, "% é a taxa de conclusão geral")
    return calculoTaxa

def iniciadosG():
    for i in range(len(DataGupy)):
        dataIn = DataGupy.iloc[i]["Data de início na trilha"]
        dataFi = DataGupy.iloc[i]["Data de finalização na trilha"]
        if dataIn != "" and dataFi != "":
            print(i, DataGupy.iloc[i]["Chefia ADP"], " iniciou")
        else:
            print(i, DataGupy.iloc[i]["Chefia ADP"], " não concluido")

def concluidosG():
    for i in range(len(DataGupy)):
        dataIn = DataGupy.iloc[i]["Data de início na trilha"]
        if dataIn != "":
            print(i, DataGupy.iloc[i]["Chefia ADP"], " concluido")

def naoIniciadosG():
    for i in range(len(DataGupy)):
        dataIn = DataGupy.iloc[i]["Data de início na trilha"]
        dataFi = DataGupy.iloc[i]["Data de finalização na trilha"]
        if dataIn == "" and dataFi == "":
            print(i, DataGupy.iloc[i]["Chefia ADP"], " Não iniciou")

# PARTE SUPPLY GO

def taxaDeConclusãoS():
    taxa = 0
    for i in range(len(DataSuplyGo)):
        info = DataSuplyGo.iloc[i]["Status Trilha"]
        if(info == "Concluído"):
            taxa = taxa + 1
    calculoTaxa = round((taxa/(len(DataSuplyGo)))*100, 2)
    print(calculoTaxa, "% é a taxa de conclusão geral")
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
        objetivo = int(input("1 - Taxa de conclusão || 2 - Iniciados || 3 - Concluidos || 4 - Não Iniciados || 5 - Sair"))
        match objetivo:
            case 1: taxaDeConclusãoG()

            case 2: iniciadosG()

            case 3: concluidosG()

            case 4: naoIniciadosG()        

taxaDeConclusãoG()