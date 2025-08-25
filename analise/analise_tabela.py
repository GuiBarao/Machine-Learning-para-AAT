import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from tabela_comparativa import lista_avaliacoes


def matrizes_avaliacoes(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    array_humanas = np.array(humanas)
    array_sistema = np.array(sistema)

    return(array_humanas, array_sistema)

def quantidade_agrupamento(avaliacoes:list, min:int, max:int) -> int:
    return len(list(filter(lambda x: (x >= min and x <= max), avaliacoes)))

def cria_graficos(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

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

    dados_graficoSistema = {
        "0-100": quantidade_agrupamento(sistema, 0, 100),
        "101-200": quantidade_agrupamento(sistema, 101, 200),
        "201-300": quantidade_agrupamento(sistema, 201, 300),
        "301-400": quantidade_agrupamento(sistema, 301, 400),
        "401-500": quantidade_agrupamento(sistema, 401, 500),
        "501-600": quantidade_agrupamento(sistema, 501, 600),
        "601-700": quantidade_agrupamento(sistema, 601, 700),
        "701-800": quantidade_agrupamento(sistema, 701, 800),
        "801-900": quantidade_agrupamento(sistema, 801, 900),
        "901-1000": quantidade_agrupamento(sistema, 901, 1000)
    }

    map_corpus = {"kaggle" : "Ensino Fundamental", "uol":"Ensino Médio"}

    
    plt.bar(list(dados_graficoHumano.keys()), list(dados_graficoHumano.values()))
    plt.title(f'Avaliações de textos do {map_corpus[corpus]} dada por humanos')
    plt.xlabel('Intervalo de avaliação')
    plt.ylabel('Quantidade de textos avaliados no intervalo')
    plt.xticks(fontsize=6)    
    plt.tight_layout()
    plt.savefig(f"testaNovoModelo\\{corpus}\\barrasHumanos.pdf", format="pdf" )
    

    plt.close()

    plt.bar(list(dados_graficoSistema.keys()), list(dados_graficoSistema.values()))
    plt.title(f'Avaliações de textos do {map_corpus[corpus]} dada pela sistema')
    plt.xlabel('Intervalo de avaliação')
    plt.ylabel('Quantidade de textos avaliados no intervalo')
    plt.xticks(fontsize=6)
    plt.tight_layout()
    plt.savefig(f"testaNovoModelo\\{corpus}\\barrasSistema.pdf", format="pdf")

    plt.close()

def medias(corpus):
    humanas, sistema = matrizes_avaliacoes(corpus)
    return (humanas.mean(), sistema.mean())

def medianas(corpus):
    humanas, sistema = matrizes_avaliacoes(corpus)
    return (np.median(humanas).item(), np.median(sistema).item())

def modas(corpus):
    humanas, sistema = matrizes_avaliacoes(corpus)

    moda_humanas = stats.mode(humanas, axis=None, keepdims=False)
    moda_sistema = stats.mode(sistema, axis=None, keepdims=False)

    return ((moda_humanas.mode.item(), moda_humanas.count.item()), (moda_sistema.mode.item(), moda_sistema.count.item()))


def main():
    #print(medias("uol"))    #humana = 480.59149722735674 | sistema = 467.13863216266174
    #print(medias("kaggle")) #humana = 502.7734627831715  | sistema = 505.0129449838188

    cria_graficos("kaggle")
    #cria_graficos("uol")

    #print(medianas("kaggle")) #humana = 500.0 | sistema = 528.0
    #print(medianas("uol")) #humana = 500.0 | sistema = 473.0

    #print(modas("kaggle"))     #humana (562, 81) | sistema (563, 6)
    #print(modas("uol"))         #humana (500, 59) | sistema (407, 7)

    pass


if __name__ == '__main__':
    main()
