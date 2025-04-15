import sys
sys.path.insert(0, 'src')

from Texto import Texto
from Modelo import Modelo

def busca():
        
    id = 0

    while(True):


        txt = Texto.xml_to_object(id, 'kaggle')
        id += 1
        print(id)
        print("---",txt.mostFrequent_sentenceLen(),"---")


def main():
    #busca()

    modelo = Modelo("geral")
    modelo.extrair_leiturabilidade("data/atributos/kaggle/leiturabilidade.csv", "kaggle")
    modelo.extrair_leiturabilidade("data/atributos/uol/leiturabilidade.csv", "uol")


    #txt = Texto.xml_to_object(2, 'kaggle')
    #print(txt.redacao)
    #print(txt.word_variationIndex())


    #modelo.extrair_sofisticacao_lexica("data/atributos/kaggle/sof_lexica.csv", "kaggle")
    #modelo.extrair_sofisticacao_lexica("data/atributos/uol/sof_lexica.csv", "uol")


if __name__ == '__main__':
    main()