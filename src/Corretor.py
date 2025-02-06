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

              

