import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from tabela_comparativa import lista_avaliacoes


def matrizes_avaliacoes(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    array_humanas = np.array(humanas)
    array_sistema = np.array(sistema)

    return(array_humanas, array_sistema)

def cria_graficos(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    labels = [str(i) for i in range(len(humanas))]

    map_corpus = {"kaggle" : "Ensino Fundamental", "uol":"Ensino Médio"}


    plt.bar(labels, humanas)
    plt.title(f'Avaliações de textos do {map_corpus[corpus]} dada por humanos')
    plt.xlabel('Indice da avaliação')
    plt.ylabel('Avaliação recebida')
    plt.xticks(np.arange(0, len(labels), 10), rotation=90, fontsize=6)    
    plt.tight_layout()
    plt.savefig(f"tabelas\\graficos\\{corpus}\\humanas.pdf", format="pdf" )

    plt.close()

    plt.bar(labels, sistema)
    plt.title(f'Avaliações de textos do {map_corpus[corpus]} dada pela sistema')
    plt.xlabel('Indice da avaliação')
    plt.ylabel('Avaliação recebida')
    plt.xticks(np.arange(0, len(labels), 10), rotation=90, fontsize=6)    
    plt.tight_layout()
    plt.savefig(f"tabelas\\graficos\\{corpus}\\sistema.pdf", format="pdf")

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

    #cria_graficos("kaggle")
    #cria_graficos("uol")

    #print(medianas("kaggle")) #humana = 500.0 | sistema = 528.0
    #print(medianas("uol")) #humana = 500.0 | sistema = 473.0

    #print(modas("kaggle"))     #humana (562, 81) | sistema (563, 6)
    #print(modas("uol"))         #humana (500, 59) | sistema (407, 7)

    pass


if __name__ == '__main__':
    main()
