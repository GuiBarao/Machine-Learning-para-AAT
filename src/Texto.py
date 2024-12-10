import xml.etree.ElementTree as ET
import nltk
from Corretor import Corretor
import pandas as pd
import math
import spacy


class Texto:
    diretorio_corpus_kaggle = 'data/corpus_kaggle.xml'
    diretorio_corpus_uol = 'data/corpus_uol.xml'
    idBase = 0
    ultimo_id = 1234
    media_palavras_corpus = 148.37165991902833
    pln = spacy.load("pt_core_news_lg")

    def __init__(self, redacao, avaliacao, uso_AM, corpus):
        self.redacao = redacao
        self.avaliacao = avaliacao
        self.uso_AM = uso_AM #treino ou teste
        self.corpus = corpus #uol ou kaggle
        self.atributos = {}
        self.id = Texto.idBase
        Texto.idBase += 1

    @staticmethod
    def diretorio_corpus(corpus):
        if corpus == 'uol':
            diretorio = Texto.diretorio_corpus_uol
        elif corpus == 'kaggle':
            diretorio = Texto.diretorio_corpus_kaggle
        else:
            exit()

        return diretorio

    #Transforma um objeto em xml e salva no arquivo corpus.xml
    def to_xml(self):

        caminho_corpus = Texto.diretorio_corpus(self.corpus)

        texto = ET.Element('texto')
        redacao = ET.SubElement(texto, 'redacao')
        avaliacao = ET.SubElement(texto, 'avaliacao')
        uso_AM = ET.SubElement(texto, 'uso_AM')
        corpus = ET.SubElement(texto, 'corpus')
        atributos = ET.SubElement(texto, 'atributos')
        id = ET.SubElement(texto, 'id')

        redacao.text = self.redacao
        avaliacao.text = str(self.avaliacao)
        uso_AM.text = self.uso_AM
        corpus.text = self.corpus

        string_atributos = ''
        for chave, valor in self.atributos.items():
            string_atributos += str(chave) + ':' + str(valor) + ';'

        atributos.text = string_atributos
        id.text = str(self.id)
        try:
            abertura_XML = ET.parse(caminho_corpus)
            raiz = abertura_XML.getroot()
        except:
            raiz = ET.Element('corpus_completo')
            abertura_XML = ET.ElementTree(raiz)
            
        raiz.append(texto)
        abertura_XML.write(caminho_corpus, encoding='utf-8', xml_declaration=True)

    #Transforma um texto xml em um objeto.
    @classmethod
    def xml_to_object(cls, id, corpus):
        caminho_corpus = Texto.diretorio_corpus(corpus)
        
        texto = Texto.buscar_texto(id, caminho_corpus)

        if (texto):
            return cls(texto.find('redacao').text, texto.find('avaliacao').text, texto.find('uso_AM').text, texto.find('corpus').text)
        else:
            return False

    #Busca um texto xml pelo id e retorna a raiz.
    @staticmethod
    def buscar_texto(id, caminho_corpus):
        arvoreXML = ET.parse(caminho_corpus)
        raiz = arvoreXML.getroot()

        for texto in raiz.findall('texto'):
            idAtual = texto.find('id').text
            if (idAtual == str(id)):
                return texto
        
        return False

    #Retorna uma lista dos tokens da redacao. Filtra os tokens de acordo com as chaves.
    def tokenizado(self, exclui_stopwords = False, exclui_especiais = False):
        tokensTexto = Texto.pln(self.redacao)

        if exclui_stopwords:
            tokensTexto = [token for token in tokensTexto if not token.is_stop]

        if exclui_especiais:
            tokensTexto = [token for token in tokensTexto if token.is_alpha]

        return tokensTexto
         
    #Retorna a lista de tokens após o processo de stemming
    def stemming(self):
        stemmer = nltk.stem.RSLPStemmer()
        return [stemmer.stem(token) for token in self.tokenizado()]

    # 1. number of characters
    def nCaracteres(self):
        return len(self.redacao)
    
    # 2. number of words
    def nPalavras(self):
        return len(self.tokenizado(exclui_especiais=True))
    
    def tamanho_palavras(self):
        palavras = self.tokenizado(exclui_especiais=True)
        return [len(word) for word in palavras]

    # 6. average word length
    def media_tamanho_palavras(self):
        return sum(self.tamanho_palavras()) / self.nPalavras()
    
    # 10. most frequent word length
    def tamanho_mais_frequente(self):
        tamanhos_palavras = self.tamanho_palavras()
        
        dict_frequencias = {tamanhos_palavras.count(tamanho) : tamanho for tamanho in tamanhos_palavras}

        maior_freq = max(dict_frequencias.keys())
        return dict_frequencias[maior_freq]
    
    #30. number of short words
    def nPalavrasCurtas(self):
        tokens = self.tokenizado(exclui_stopwords=True, exclui_especiais=True)

        #tam_maximo_curtas = Corretor.media_tamanho_palavras()
        tam_maximo_curtas = 6

        tam = list(map(len, tokens))
        curtas = list(filter(lambda x: x <= tam_maximo_curtas, tam))

        return len(curtas)
        
    # 19. number of different PoS tags
    def n_diferentes_posTags(self):
        tokens = self.tokenizado(exclui_especiais=True)
        pos_tags = [token.pos_ for token in tokens]

        set_tags = set(pos_tags)
        
        return len(set_tags)
    
    def n_etiqueta(self, tag):
        tokens_pos = self.tokenizado(etiquetados=True, exclui_especiais=True)
        pos_tags = [token[1] for token in tokens_pos]

        return pos_tags.count(tag)

    def erros_ortograficos(self):
        vocabulario = Corretor.vocabulario_textual()
        tokens = self.tokenizado(exclui_especiais=True)

        return [word for word in tokens if word not in vocabulario]
    
    # 32. number of spellchecking errors
    def avaliacao_ortografica(self):
        erros = self.erros_ortograficos()
        correcoes = [Corretor.correcao_ortografica(erro) for erro in erros]
        
        pontuacoes = [correcao[2] for correcao in correcoes]

        return sum(pontuacoes)

    def vocabulario(self):

        tokens = self.tokenizado(exclui_stopwords=True, exclui_especiais=True)
        frequencias = pd.read_csv('data\\frequencias.csv')

        tokens_frequentes = frequencias[frequencias['palavra'].isin(tokens)]

        return len(tokens) - len(tokens_frequentes)
    
    #Atributos de distância (Cos) e (Euclid)
    
    def janelas_deslizantes(self):
        
        tokens = self.tokenizado()
        palavras_texto = [token.text for token in tokens]

        tam_janela = int(len(palavras_texto) * 0.25) + 1
        tam_janela = max(tam_janela, 1)

        #   25          = 10
        #   tam_janela  = passo
        passo = math.ceil((tam_janela*10)/25)

        janelas = []

        inicio = 0 
        
        fim = tam_janela

        while(fim <= len(palavras_texto)):

            janelas.append(palavras_texto[inicio : fim])
            
            inicio += passo
            fim += passo

            if (fim > len(palavras_texto)):

                fim = len(palavras_texto)
                janelas.append(palavras_texto[inicio : fim])
                break
        
        janelas_strings = [' '.join(janela) for janela in janelas]

        return janelas_strings

    def cossenos(self, qualquer_ponto = False, vizinhos = False):
        janelas = self.janelas_deslizantes()

        similaridades = []

        if (vizinhos and not qualquer_ponto):
            indice = 1

            while(indice < len(janelas)):
                cosseno = Corretor.similaridade_cosseno(janelas[indice-1], janelas[indice])
                similaridades.append(cosseno)
                indice+=1

        
        if(qualquer_ponto and not vizinhos):
            for i, janela in enumerate(janelas):
                for j in range(i+1, len(janelas)):
                    similaridades.append(Corretor.similaridade_cosseno(janela, janelas[j]))

        return similaridades
    
    def euclid(self, qualquer_ponto = False, vizinhos = False):
        janelas = self.janelas_deslizantes()

        distancias = []

        if (vizinhos and not qualquer_ponto):
            distancias = [Corretor.distancia_euclid(janelas[i-1], janela) for i, janela in enumerate(janelas) if i != 0]

        if (qualquer_ponto and not vizinhos):
            for i, janela in enumerate(janelas):
                for j in range(i+1, len(janelas)):
                    distancias.append(Corretor.distancia_euclid(janela, janelas[j]))

        return distancias

    # -----Euclid-----

    # 21. minimum distance between neighboring points (Euclid)
    def menor_distancia_euclid(self):
        distancias = self.euclid(vizinhos=True)
        return min(distancias)
    
    # 35. maximum distance between neighboring points (Euclid)
    def maior_distancia_euclid(self):
        distancias = self.euclid(vizinhos=True)
        return max(distancias)

    # 34. index (minimum distance/maximum distance) (Euclid)
    def euclid_index(self):
        return self.maior_distancia_euclid() / self.menor_distancia_euclid()

    # 40. average distance between any two points (Euclid)
    def distancia_media_euclid(self):
        distancias = self.euclid(qualquer_ponto=True)
        return sum(distancias) / len(distancias)

    #-----Cosseno-----

    #39. maximum distance between neighboring points (Cos)
    def maior_distancia_cosseno(self, qualquer_ponto = False, vizinhos = False):
        return min(self.cossenos(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto))

    # X. minimum distance between neighboring points (Cos)
    def menor_distancia_cosseno(self, qualquer_ponto = False, vizinhos = False):
        return max(self.cossenos(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto))

    # 36. index (minimum distance/maximum distance) (Cos)
    # 31. index (minimum distance/maximum distance) (Cos)
    def cosseno_index(self, qualquer_ponto = False, vizinhos = False):
        menor = self.menor_distancia_cosseno(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto)
        maior = self.maior_distancia_cosseno(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto)
        return menor/maior
    
    # 33. average distance between any two points (Cos)
    def media_distancia_cosseno(self,qualquer_ponto = False, vizinhos = False):
        similaridades = self.cossenos(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto)
        distancias = [1 - valor for valor in similaridades]
        return sum(distancias)/len(distancias)
    
    # 48. maximum difference between any two points (Cos)
    def maior_diferenca_cosseno(self, qualquer_ponto = False, vizinhos = False):
        similaridades = self.cossenos(vizinhos = vizinhos, qualquer_ponto=qualquer_ponto)
        distancias = [1 - valor for valor in similaridades]
        diferencas = []

        for i, distancia in enumerate(distancias):
            for j in range(i+1, len(distancias)):
                diferencas.append(abs(distancia - distancias[j]))

        return max(diferencas)

    #---PoS Tags---

    # 12. number of adjectives
    def nADJ(self):
        tokens = self.tokenizado(exclui_especiais=True)
        return len([token for token in tokens if token.pos_ == 'ADJ'])

    # 26. number of adverbs
    def nADV(self):
        tokens = self.tokenizado(exclui_especiais=True)
        return len([token for token in tokens if token.pos_ == 'ADV'])
    
    # 25. number of determiners
    def nDET(self):
        tokens = self.tokenizado(exclui_especiais=True)
        return len([token for token in tokens if token.pos_ == 'DET'])
    
    # 44. number of verbs - base form
    def nVERB(self):
        tokens = self.tokenizado(exclui_especiais=True)
        return len([token for token in tokens if token.pos_ == 'VERB'])
    
    #???

    # 4. number of superlative adjectives
    def nSuperlativos(self):
        tokens = self.tokenizado(exclui_especiais=True, etiquetados=True)
        
        return len(Corretor.identifica_superlativos(tokens))

    # 5. number of predeterminers
    def nPreDeterminantes(self):
        tokens = self.tokenizado(exclui_especiais=True, etiquetados = True)
        predeterminantes = Corretor.identifica_predeterminantes(tokens)
        return len(predeterminantes)
    
    # 7. number of existential there’s
    def nConstrucoes_existenciais(self):
        tokens = self.tokenizado(exclui_especiais=True)
        return len(Corretor.identifica_existenciais(tokens))
    
    # 8. number of genitive markers
    def nPosse(self):
        return len(Corretor.identifica_posse(self.tokenizado(exclui_especiais=True)))
    