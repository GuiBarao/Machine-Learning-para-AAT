from spellchecker import SpellChecker
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


class Corretor:


    @staticmethod
    def vocabulario_textual():
        with open('data/dicionario.txt','r', encoding='utf8') as f:
            palavrasPT = f.readlines()
        
            #Extrai das linhas o caractere '\n' e retorna.
            return set([linha.strip('\n') for linha in palavrasPT])

    
    @staticmethod
    def correcao_ortografica(palavra_errada):
        spell = SpellChecker(language='pt')
    
        correcao = spell.correction(palavra_errada)

        peso = Corretor.distancia_euclid(palavra_errada, correcao)

        return (correcao, peso)
        
        
       

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
    def identifica_adjetivos_superlativos(tokens):
        sufixos = ['íssimo', 'íssima', 'íssimos', 'íssimas', 
                   'érrimo', 'érrima', 'érrimos', 'érrimas',
                   'ílimo', 'ílima', 'ílimo']
        
        adverbios_formadores = ['muito', 'extremamente', 'super', 'altamente', 'imensamente', 
                                'incrivelmente', 'excepcionalmente', 'consideravelmente', 
                                'absolutamente', 'profundamente', 'notavelmente', 'surpreendentemente', 
                                'excessivamente', 'desmedidamente', 'bastante', 'espantosamente', 'extraordinariamente', 
                                'fenomenalmente', 'enormemente', 'grandemente', 'maravilhosamente', 'formidavelmente', 
                                'admiravelmente', 'incomparavelmente', 'deslumbrantemente', 'singularmente', 'ultra', 
                                'mega', 'extremoso', 'suficientemente', 'desproporcionalmente', 'altissimamente', 
                                'majestosamente', 'poderosamente', 'obscenamente', 'diabolicamente', 'categórica', 
                                'absolutamente', 'imensamente', 'esplendidamente', 'absurdamente', 'tão', 
                                'razoavelmente', 'indiscutivelmente', 'irrevogavelmente', 'primorosamente', 
                                'encantadoramente', 'espiritualmente', 'redondamente', 'alucinantemente', 'fabulosamente']

        superlativos = []

        token_anterior = ''

        for token, tag in tokens:
            
            if(tag == 'ADJ'):
                superlativo = False

                for sufixo in sufixos:

                    if token.endswith(sufixo):
                        superlativos.append(token)
                        superlativo = True
                        break
                
                if not superlativo:
                    for adv in adverbios_formadores:
                        if adv == token_anterior:
                            superlativos.append(token)
                            superlativo = True
                            break

            token_anterior = token

        return superlativos

    @staticmethod
    def identifica_predeterminantes(tokens):
        predeterminantes = []

        for i, tupla in enumerate(tokens):
            token = tupla[0]
            tag = tupla[1]

            try:
                proxima_tag = tokens[i+1][1]
            except:
                continue
            
            if tag == 'DET' and proxima_tag == 'DET':
                predeterminantes.append(token)
            
        return predeterminantes

    @staticmethod
    def identifica_existenciais(tokens):
        verbos_existenciais = [ "haver", "há", "havia", "houve", "haveria", "haverá", "haja", "houvesse", "houver", "houveram",
                                "existir", "existe", "existia", "existiu", "existirá", "existiria", "exista", "existisse", "existirão",
                                "ter", "tem", "tinha", "teve", "teria", "terá", "tenha", "tivesse", "terão"]
        

        lemmatizados = [(token, token.lemma_) for token in tokens]
        verbos = [(token.text, lemma) for token, lemma in lemmatizados if token.pos_ == 'VERB']
        return [verbo for verbo, lemma in verbos if lemma in verbos_existenciais]

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
    
    @staticmethod
    def identifica_adverbios_superlativos(tokens):
        pass
