#tratamento dos dados das planilhas
import numpy as np
import pandas as pd

data = pd.read_excel(".\Participants-36809.xlsx", index_col=None, keep_default_na=False , na_values= 'nan')

def taxaDeConclusão():
    taxa = 0
    for i in range(len(data)):
        info = data.iloc[i]["Status de realização"]
        if(info == "Concluído"):
            taxa = taxa + 1
    calculoTaxa = round((taxa/(len(data)))*100, 2)
    print(calculoTaxa, "% é a taxa de conclusão geral")

def iniciados():
    taxa = 0
    for i in range(len(data)):
        dataIn = data.iloc[i]["Data de início na trilha"]
        dataFi = data.iloc[i]["Data de finalização na trilha"]
        if dataIn != "" and dataFi != "":
            print(i, data.iloc[i]["Chefia ADP"], " iniciou")
        else:
            print(i, data.iloc[i]["Chefia ADP"], " não concluido")

def concluidos():
    for i in range(len(data)):
        dataIn = data.iloc[i]["Data de início na trilha"]
        if dataIn != "":
            print(i, data.iloc[i]["Chefia ADP"], " concluido")

def naoIniciados():
    for i in range(len(data)):
        dataIn = data.iloc[i]["Data de início na trilha"]
        dataFi = data.iloc[i]["Data de finalização na trilha"]
        if dataIn == "" and dataFi == "":
            print(i, data.iloc[i]["Chefia ADP"], " Não iniciou")

def mensagem():
    print()

def run():
    objetivo = int(input("1 - Taxa de conclusão || 2 - Iniciados || 3 - Concluidos || 4 - Não Iniciados || 5 - Sair"))
    while objetivo != 5:
        match objetivo:
            case 1: taxaDeConclusão()

            case 2: iniciados()

            case 3: concluidos()

            case 4: naoIniciados()
    run()
        
run()