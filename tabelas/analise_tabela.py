import numpy as np
from tabela_comparativa import lista_avaliacoes


def medias(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    array_humanas = np.array(humanas)
    array_sistema = np.array(sistema)

    return (array_humanas.mean(), array_sistema.mean())

def main():
    #print(medias("uol"))    #humana = 480.59149722735674 | sistema = 467.13863216266174

    #print(medias("kaggle")) #humana = 502.7734627831715  | sistema = 505.0129449838188

    pass


if __name__ == '__main__':
    main()
