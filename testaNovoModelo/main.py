import sys
sys.path.insert(0, 'src')

from Modelo import Modelo
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import joblib
import matplotlib.pyplot as plt


def divisao_features(caminho_csv):

    array = np.loadtxt(caminho_csv, delimiter=",")

    #remove a coluna de avaliação (ultima)  
    x = array[:, :-1]
    y = array[:, -1]    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=62)

    return (x_train, x_test, y_train, y_test)

def treinar_modelo_randomForest(atributos, avaliacao):

    modelo = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=317)

    #modelo = RandomForestRegressor(
    #n_estimators=600,
    #max_depth=None,            
    #min_samples_leaf=1,        
    #min_samples_split=2,
    #max_features="sqrt",
    #bootstrap=True,
    #n_jobs=-1,
    #random_state=317
    #)
#

    modelo.fit(atributos,avaliacao)

    return modelo 


def treinar_modelo_boosting(atributos, avaliacao):

    modelo = GradientBoostingRegressor(
        loss="huber",
        learning_rate=0.04,
        n_estimators=1400,
        max_depth=4,
        subsample=0.8,
        random_state=317
    )

    modelo.fit(atributos, avaliacao)
    return modelo

def criar_modelo(caminho_csv, caminho_modelo, algoritmo='random_forest'):

    x_treino, x_teste, y_treino, y_teste = divisao_features(caminho_csv)

    if algoritmo == 'random_forest':
        modelo = treinar_modelo_randomForest(x_treino, y_treino)
        joblib.dump(modelo, caminho_modelo)
        return modelo.score(x_teste, y_teste)
    else:
        modelo = treinar_modelo_boosting(x_treino, y_treino)
        joblib.dump(modelo, caminho_modelo)
        return modelo.score(x_teste, y_teste)




def quantidade_agrupamento(avaliacoes:list, min:int, max:int) -> int:
    return len(list(filter(lambda x: (x >= min and x <= max), avaliacoes)))

def cria_graficos(corpus):
    humanas = np.loadtxt('testaNovoModelo\\atributos\\kaggle\\geralFiltrado.csv', delimiter=',')[:, -1]

    dados_graficoHumano = {
        "0-100": quantidade_agrupamento(humanas, 0, 100),
        "101-200": quantidade_agrupamento(humanas, 101, 200),
        "201-300": quantidade_agrupamento(humanas, 201, 300),
        "301-400": quantidade_agrupamento(humanas, 301, 400),
        "401-500": quantidade_agrupamento(humanas, 401, 500),
        "501-600": quantidade_agrupamento(humanas, 501, 600),
        "601-700": quantidade_agrupamento(humanas, 601, 700),
        "701-800": quantidade_agrupamento(humanas, 701, 800),
        "801-900": quantidade_agrupamento(humanas, 801, 900),
        "901-1000": quantidade_agrupamento(humanas, 901, 1000),
    }


    map_corpus = {"kaggle" : "Ensino Fundamental", "uol":"Ensino Médio"}

    
    plt.bar(list(dados_graficoHumano.keys()), list(dados_graficoHumano.values()))
    plt.title(f'Avaliações de textos do {map_corpus[corpus]} dada por humanos')
    plt.xlabel('Intervalo de avaliação')
    plt.ylabel('Quantidade de textos avaliados no intervalo')
    plt.xticks(fontsize=6)    
    plt.tight_layout()
    plt.savefig(f"testaNovoModelo\\{corpus}\\barrasDatasetInteiro.pdf", format="pdf" )
    

    plt.close()



def main():

    #tipos = ["autocorrelacao_espacial", "coerencia", "dados_espaciais",
    #    "diversidade_lexica", "gramatica", "leiturabilidade", "mecanica", "pos_tags", "sofisticacao_lexica"]
    
    #modelo = Modelo()

    #modelo.extrair_geral(tipos=tipos, corpus='kaggle')
    #cria_graficos("kaggle")

    print(criar_modelo("testaNovoModelo\\atributos\\kaggle\\geralFiltrado.csv", 
                 "testaNovoModelo\\kaggle\\geral.pkl", 
                 algoritmo="4ryewef"))

    


if __name__ == '__main__':
    main()