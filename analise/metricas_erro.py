from tabela_comparativa import lista_avaliacoes
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, cohen_kappa_score
import numpy as np
import pandas as pd

def MAE(humanas, sistema):
    return mean_absolute_error(humanas, sistema)

def MSE(humanas, sistema):
    return mean_squared_error(humanas, sistema)

def RMSE(humanas, sistema):
    return np.sqrt(MSE(humanas, sistema))

def R_2(humanas, sistema):
    return r2_score(humanas,sistema)

def kappa_quadratico(humanas, sistema: list[int]) -> float:

    return cohen_kappa_score(humanas, sistema, weights="quadratic")



def cria_planilha(corpus:str):
    humanas, sistema = lista_avaliacoes(corpus)

    dados = {
        "MAE": MAE(humanas,sistema),
        "MSE": MSE(humanas,sistema),
        "RMSE": RMSE(humanas,sistema),
        "R²": R_2(humanas,sistema),
        "KQ": kappa_quadratico(humanas,sistema)
    }

    df = pd.DataFrame([dados])

    df.to_excel(f"analise\\planilhas\\{corpus}\\metricas_{corpus}.xlsx")

def main():

    cria_planilha("uol")
    cria_planilha("kaggle")


if __name__ == "__main__":
    main()