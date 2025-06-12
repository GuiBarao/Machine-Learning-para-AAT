import numpy as np
import matplotlib.pyplot as plt
from tabela_comparativa import lista_avaliacoes


def medias(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    array_humanas = np.array(humanas)
    array_sistema = np.array(sistema)

    return (array_humanas.mean(), array_sistema.mean())

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
    plt.savefig(f"tabelas\\graficos\\{corpus}\\sistema.pdf", format="pdf" )

    plt.close()

def main():
    #print(medias("uol"))    #humana = 480.59149722735674 | sistema = 467.13863216266174
    #print(medias("kaggle")) #humana = 502.7734627831715  | sistema = 505.0129449838188

    #cria_graficos("kaggle")
    #cria_graficos("uol")
    pass


if __name__ == '__main__':
    main()
