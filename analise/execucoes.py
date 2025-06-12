import pandas as pd
import numpy as np
from tabela_comparativa import divisao_features
import joblib


def avaliacoes(lista_atributos, modelo):

    max = 10

    resultados = [modelo.predict([lista_atributos])[0] for i in range(max)]

    return resultados




def execucoes(corpus):
    x_teste = divisao_features(f"data\\atributos\\{corpus}\\geral.csv")[1]
    
    modelo = joblib.load(f"modelos_treinados\\{corpus}\\geral.pkl")

    matriz_resultados = np.array(list(map(lambda atributos: avaliacoes(atributos, modelo), x_teste)))

    df = pd.DataFrame(matriz_resultados)

    df.to_excel(f"analise\\planilhas\\{corpus}.xlsx")

    

  


def main():
    #execucoes("kaggle")
    execucoes("uol")

if __name__ == '__main__':
    main()