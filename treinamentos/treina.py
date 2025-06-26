from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib
import pandas as pd
import time
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, cohen_kappa_score

#Seeds do sistema
#randomSeed_split = 62
#randomSeed_modelo = 317

def divisao_features(caminho_csv, seed):

    array = np.loadtxt(caminho_csv, delimiter=",")

    #remove a coluna de avaliação (ultima)  
    x = array[:, :-1]
    y = array[:, -1]    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)

    return (x_train, x_test, y_train, y_test)


def treinar_modelo(atributos, avaliacao, seed):
    modelo = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=seed)

    modelo.fit(atributos,avaliacao)

    return modelo 

def criar_modelo(corpus, nomeModelo, splitSeed = 62, modelSeed = 317):

    caminho_csv = f'data\\atributos\\{corpus}\\geral.csv'
    caminho_modelo = f'treinamentos\\modelos\\{corpus}\\{nomeModelo}.pkl'

    x_treino, x_teste, y_treino, y_teste = divisao_features(caminho_csv, splitSeed)

    inicio = time.time()
    modelo = treinar_modelo(x_treino, y_treino, modelSeed)
    fim = time.time()

    #joblib.dump(modelo, caminho_modelo)

    return {"timeStamp": fim-inicio, "xTeste": x_teste, "yTeste": y_teste, "modelo":modelo}

def metricasModelo(modelo: RandomForestRegressor, labelX, labelY):

    humanas = labelY
    sistema = modelo.predict(labelX)

    humanas_int = np.round(humanas).astype(int)
    sistema_int = np.round(sistema).astype(int)

    return {"MAE": mean_absolute_error(humanas,sistema), 
            "MSE": mean_squared_error(humanas,sistema), 
            "RMSE": np.sqrt(mean_squared_error(humanas,sistema)), 
            "R_2": r2_score(humanas,sistema), 
            "kappa_quadratico": cohen_kappa_score(humanas_int, sistema_int, weights="quadratic")}
    

def registrar_modelo(nomeModelo, timestamp, metricas, splitSeed = 62, modelSeed = 317):
    dados = {
        "nomeModelo": nomeModelo,
        "seed de divisão de features": splitSeed,
        "seed de treinamento": modelSeed,
        "timestamp de execução": timestamp,
        "MAE": metricas["MAE"], 
        "MSE": metricas["MSE"], 
        "RMSE": metricas["RMSE"], 
        "R_2": metricas["R_2"], 
        "kappa_quadratico": metricas["kappa_quadratico"]
   }
    df_novo = pd.DataFrame([dados])

    caminho_excel = "treinamentos\\modelos.xlsx"

    if os.path.exists(caminho_excel):
        df_existente = pd.read_excel(caminho_excel)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = df_novo

    df_final.to_excel(caminho_excel, index=False)


def main():

    corpus = ["kaggle", "uol"]

    treinamentos = {
        "modelo1" : {"split":62, "modelo":317},
        "modelo2" : {"split": 54, "modelo":33},
        "modelo3" : {"split": 92, "modelo": 12}
    }

    for c in corpus:

        for modelo in treinamentos.keys():
            seedModelo = treinamentos[modelo]
            nomeModelo = f'{c}_{modelo}'

            dict_analise = criar_modelo(corpus=c, nomeModelo=nomeModelo, 
                         splitSeed=seedModelo["split"], modelSeed=seedModelo["modelo"])
            
            dict_metricas = metricasModelo(modelo = dict_analise["modelo"], 
                                           labelX = dict_analise["xTeste"],
                                           labelY = dict_analise["yTeste"])

            registrar_modelo(nomeModelo=nomeModelo,
                             metricas = dict_metricas,
                             timestamp=dict_analise["timeStamp"], 
                             splitSeed=seedModelo["split"], 
                             modelSeed=seedModelo["modelo"])

if __name__ == "__main__":
    main()