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

taxaDeConclusão()