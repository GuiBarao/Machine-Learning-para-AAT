from spellchecker import SpellChecker
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


class Corretor:



    @staticmethod
    def similaridade_cosseno(texto1, texto2):
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform([texto1,texto2])
        similaridade = cosine_similarity(matriz[0:1], matriz[1:2])
        return float(similaridade[0][0])
    
    @staticmethod
    def distancia_euclid(texto1, texto2):
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform([texto1,texto2])
        distancias = euclidean_distances(matriz[0:1], matriz[1:2])
        return float(distancias[0][0])

    @staticmethod
    def media_tamanho_palavras():
        frequencias = pd.read_csv('data\\frequencias.csv')

        tam_palavras =  frequencias['palavra'].apply(lambda x: len(str(x)))       

        soma = tam_palavras.sum()

        n_palavras = frequencias["palavra"].count()

        return int(soma/n_palavras)



    @staticmethod
    def identifica_posse(tokens):
        verbos_posse = [
                        "ter", "tenho", "tens", "tem", "temos", "têm",
                        "tinha", "tinhas", "tinha", "tínhamos", "tinham",
                        "terei", "terás", "terá", "teremos", "terão",
                        "tenha", "tenhas", "tenha", "tenhamos", "tenham",

                        "possuir", "possuo", "possuis", "possui", "possuímos", "possuem",
                        "possuía", "possuías", "possuía", "possuíamos", "possuíam",
                        "possuirei", "possuirás", "possuirá", "possuiremos", "possuirão",
                        "possua", "possuas", "possua", "possuamos", "possuam",

                        "pertencer", "pertenço", "pertences", "pertence", "pertencemos", "pertencem",
                        "pertencia", "pertencías", "pertencia", "pertencíamos", "pertenciam",
                        "pertencerei", "pertencerás", "pertencerá", "pertenceremos", "pertencerão",
                        "pertença", "pertenças", "pertença", "pertençamos", "pertençam"]

        return [token for token in tokens if token.text in verbos_posse]                

