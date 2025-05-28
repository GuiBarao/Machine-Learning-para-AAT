import sys
sys.path.insert(0, 'src')

from Modelo import Modelo
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib


def divisao_features(caminho_csv):

    array = np.loadtxt(caminho_csv, delimiter=",")

    #remove a coluna de avaliação (ultima)  
    x = array[:, :-1]
    y = array[:, -1]    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=62)

    return (x_train, x_test, y_train, y_test)

def treinar_modelo(atributos, avaliacao):
    modelo = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=317)

    modelo.fit(atributos,avaliacao)

    return modelo 

def criar_modelo(caminho_csv, caminho_modelo):

    x_treino, x_teste, y_treino, y_teste = divisao_features(caminho_csv)
    modelo = treinar_modelo(x_treino, y_treino)

    #joblib.dump(modelo, caminho_modelo)

    return modelo.score(x_teste, y_teste)

def main():

    #tipos = ["autocorrelacao_espacial", "coerencia", "dados_espaciais",
    #    "diversidade_lexica", "gramatica", "leiturabilidade", "mecanica", "pos_tags", "sofisticacao_lexica"]
    
    #modelo = Modelo()

    #modelo.extrair_geral(tipos, "uol")

    corpus = "kaggle"
    avaliacao = criar_modelo(f"data/atributos/{corpus}/geral.csv", f"modelos_treinados/{corpus}/geral.pkl")
    print(avaliacao)

    #modelo_carregado = joblib.load("modelos_treinados\kaggle\geral.pkl")

    


if __name__ == '__main__':
    main()