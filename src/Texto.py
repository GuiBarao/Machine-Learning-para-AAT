import xml.etree.ElementTree as ET
import nltk
from Corretor import Corretor
import pandas as pd
import math
import spacy
import syllapy
import math
from spellchecker import SpellChecker


class Texto:
    diretorio_corpus_kaggle = 'data/corpus_kaggle.xml'
    diretorio_corpus_uol = 'data/corpus_uol.xml'
    diretorio_dicionario = 'data/dicionario.txt'
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
    def tokenizado(self, exclui_stopwords = False, exclui_especiais = False, lower = False):
        texto = str(self.redacao).replace('\n', ' ')

        #Elimina caracteres de controle
        mapa_flags = '\n\t\r\x0b\x0c'
        tabela = str.maketrans('','',mapa_flags)
        texto_semFlags = texto.translate(tabela)
        
        tokensTexto = Texto.pln(texto_semFlags)
        
        if exclui_stopwords:
            tokensTexto = [token for token in tokensTexto if not token.is_stop]

        if exclui_especiais:
            tokensTexto = [token for token in tokensTexto if token.is_alpha]

        tokensTexto = [token.text for token in tokensTexto]

        if lower:
            tokensTexto = [token.lower() for token in tokensTexto]

        return tokensTexto
    
    #Retorna uma Lista de tuplas token, pos
    def tokenizado_pos(self):
        tokens = Texto.pln(self.redacao)

        return [(token.text, token.pos_) for token in tokens]

    #Retorna a lista de tokens após o processo de stemming
    def stemming(self):
        stemmer = nltk.stem.RSLPStemmer()
        return [stemmer.stem(token) for token in self.tokenizado()]

    # 1. number of characters
    def nChar(self):
        return len(self.redacao)
    
    # 2. number of words
    def nWords(self):
        return len(self.tokenizado(exclui_especiais=True, exclui_stopwords=True))
    
    def nSyllables_eachWord(self):
        tokens = self.tokenizado(exclui_especiais=True, exclui_stopwords=True)
        contagem_silabas = list(map(syllapy.count, tokens))
        return contagem_silabas

    #3. number of long words
    def nLongWords(self, min_nSilabas = 4):
        contagem = self.nSyllables_eachWord()
        longas = [c for c in contagem if c >= min_nSilabas]
        return len(longas)
    
    #4. number of short words
    def nShortWords(self, max_nSilabas = 3):
        contagem = self.nSyllables_eachWord()
        curtas = [c for c in contagem if c <= max_nSilabas]
        return len(curtas)    
    
    def tamanho_palavras(self):
        palavras = self.tokenizado(exclui_especiais=True)
        return [len(word) for word in palavras]

    # 5. most frequent word length
    def most_frequent_wordLen(self):
        tamanhos_palavras = self.tamanho_palavras()
        
        dict_frequencias = {tamanhos_palavras.count(tamanho) : tamanho for tamanho in tamanhos_palavras}

        maior_freq = max(dict_frequencias.keys())
        return dict_frequencias[maior_freq]

    # 6. average word length
    def average_wordLen(self):
        return sum(self.tamanho_palavras()) / self.nWords()
        
    
    def sentences(self):
        pontos = ['.','!','?']
        sentencas = []
        tokens = self.tokenizado()

        sentenca_aux = []
        for token in tokens:

            if token in pontos:
                sentencas.append(sentenca_aux)
                sentenca_aux = []
            else:
                if token.isalpha():
                    sentenca_aux.append(token)
                
        return sentencas

    #7. number of sentences
    def nSentences(self):
        return len(self.sentences())

    #8. number of long sentences
    def nLongSentences(self, nPalavras_minimo = 20):
        frases = self.sentences()
        cont = 0
        for frase in frases:
            if len(frase) >= nPalavras_minimo:
                cont+=1
        
        return cont
    
    #9. number of short sentences
    def nShortSentences(self, nPalavras_maximo = 10):
        frases = self.sentences()
        cont = 0
        for frase in frases:
            if len(frase) <= nPalavras_maximo:
                cont+=1
        
        return cont
    
    #10. most frequent sentence length 
    def mostFrequent_sentenceLen(self):
        frases = self.sentences()
        tamanhos = [len(frase) for frase in frases]
        
        dict_frequencias = {tam : tamanhos.count(tam) for tam in set(tamanhos)}
        mais_frequente = max(dict_frequencias, key=dict_frequencias.get)
        return mais_frequente

    #11. average sentence length
    def average_sentenceLen(self):
        return self.nWords()/len(self.sentences())
    
    #12. number of different words
    def nUniqueWords(self):
        words = self.tokenizado(exclui_especiais=True, exclui_stopwords=True)
        return len(set(words))

    #13. number of stopwords.
    def nStopWords(self):
        tokens = self.tokenizado(exclui_especiais=True)
        tokens_semStop = self.tokenizado(exclui_especiais=True, exclui_stopwords=True)

        return len(tokens) - len(tokens_semStop)


    def nComplexWords(self):
        tokens = self.tokenizado(exclui_stopwords=True, exclui_especiais=True, lower=True)

        freq = pd.read_csv('data\\frequencias.csv')
        return self.nWords() - freq['palavra'].isin(tokens).sum()

    #14. Gunning Fog index
    def gunningFog(self):
        return 0.4 * ((self.nWords() / self.nSentences()) + 100 * (self.nComplexWords() / self.nWords()))
        
    #15. Flesch reading ease
    def flesch_readindEase(self):
        return 226 - 1.04 * (self.nWords() / self.nSentences()) - 72 * (sum(self.nSyllables_eachWord()) / self.nWords())
    
    #16. Flesch Kincaid grade level,
    def flesch_kincaid(self):
        return 0.36 * (self.nWords() / self.nSentences()) + 10.4 * (sum(self.nSyllables_eachWord()) / self.nWords()) - 18
        
    #17. Dale-Chall readability formula
    def dale_chall(self):
        percent_ComplexWords = (self.nComplexWords() / self.nWords()) * 100
        return (0.1579 * percent_ComplexWords) + (0.0496 * self.average_sentenceLen()) + 3.6365

    def nLetters(self):
        text = self.redacao
        return sum(c.isalpha() for c in text)

    #18. automated readability index
    def automated_readabilityIndex(self):
        return (4.6 * (self.nLetters() / self.nWords()) + 
                0.44 * (self.nWords() / self.nSentences()) - 20)

    #19. simple measure of Gobbledygook 
    #adaptado
    def simple_gobbledygook(self):
        return math.sqrt(1.043 * (30 * self.nComplexWords() / self.nSentences()) + 3.1291)

    #20. LIX
    def lix(self):
        return ((self.nComplexWords() / self.nWords()) * 100) + self.average_sentenceLen()
    
    def nWordTypes(self):
        return len(set(self.tokenizado(exclui_especiais=True, exclui_stopwords=True)))

    #21. word variation index
    def word_variationIndex(self):

        numerador = math.log(self.nWords(), 10)
        denominador = math.log(2 - math.log(self.nUniqueWords(), 10) / math.log(self.nWords(), 10), 10)

        return  numerador / denominador
    
    #23. type-token-ratio
    def typeToken_ratio(self, tipo = 1):
            return self.nWords() / self.nWordTypes()
    
    #24. Guiraud’s index
    def guiraud_index(self):
        return self.nWordsTypes() / math.sqrt(self.nWords())
    
    #25. Yule’s K
    def yule_K(self):

        tokens = self.tokenizado(exclui_especiais=True, exclui_stopwords=True)
        dict_freq = {token : tokens.count(token) for token in tokens}
        
        maior_freq = max(dict_freq.values())

        Vr = [None]
        i = 1
        while(i <= maior_freq):

            r = list(dict_freq.values()).count(i)
            Vr.append(r)
            i+=1

        somatorio = 0
        for i, freq_Words in enumerate(Vr):
            if i == 0:
                continue

            somatorio += (i * i) * freq_Words

        numerador = somatorio - self.nWords()
        
        return math.pow(10,4) * numerador / math.pow(self.nWords(), 2)
    
    #27. hapax legomena - number of words occurring only once in a text, 
    def hapax_legomena(self):
        return self.nUniqueWords()

    def nAdvanced_wordTypes(self):
        tokens = self.tokenizado(exclui_stopwords=True, exclui_especiais=True, lower=True)

        set_tokens = set(tokens)

        freq = pd.read_csv('data\\frequencias.csv')

        return len(set_tokens) - freq['palavra'].isin(set_tokens).sum()

    #28. advanced Guiraud.
    def advanced_guiraud(self):

        return self.nAdvanced_wordTypes() / math.sqrt(self.nWords())
       
    #29. number of different PoS tags
    def n_differents_posTags(self):
        tokensPos = self.tokenizado_pos()
        
        posTags = [pos for _, pos in tokensPos]

        set_tags = set(posTags)
        
        return len(set_tags)
    

    def count_of_tag(self, searched_tag):
        tokensPos = self.tokenizado_pos()
        
        posTags = [pos for _, pos in tokensPos]

        count = 0

        for tag in posTags:
            if(tag == searched_tag):
                count+=1

        return count

    #33. coordinating conjunction
    def n_coordinating_conjunction(self):
        return self.count_of_tag("CCONJ")
  
    
    #34. numeral
    def n_numeral(self):
        return self.count_of_tag("NUM")

    #35. determiner
    def n_determiner(self):
        return self.count_of_tag("DET")
    
    #36. existential there
    def n_existencial(self):
        verbos_existenciais = [ "haver", "há", "havia", "houve", "haveria", "haverá", "haja", "houvesse", "houver", "houveram",
                                "existir", "existe", "existia", "existiu", "existirá", "existiria", "exista", "existisse", "existirão",
                                "ter", "tem", "tinha", "teve", "teria", "terá", "tenha", "tivesse", "terão"]
        
        tokens = self.tokenizado(exclui_especiais=True, lower=True)

        count = 0
        for token in tokens:
            if(token in verbos_existenciais):
                count += 1

        return count

    #38. adjective
    def n_adjective(self):
        return self.count_of_tag("ADJ")

    @staticmethod
    def set_dicionario():
        with open (Texto.diretorio_dicionario, 'r', encoding='utf-8') as arq:
            lista = arq.readlines()

        palavras = [linha.strip('\n') for linha in lista]

        return set(palavras)

    def nomes_proprios(self):
        tokensTexto = Texto.pln(self.redacao)
        nomes = [entidade.text.lower() for entidade in tokensTexto.ents if entidade.label_ == "PER"]
        
        nomes_maisculos_e_minusculos = []

        for nome in nomes:
            nomes_maisculos_e_minusculos.append(nome)
            nomes_maisculos_e_minusculos.append(nome.capitalize())


        return list(set(nomes_maisculos_e_minusculos))


    #65. number of spellchecking errors  
    def n_speelChecking_errors(self):        
        tokens = self.tokenizado(exclui_especiais=True, lower=True)

        cont = 0

        dicionario_set = Texto.set_dicionario()
        nomes_proprios = self.nomes_proprios()

        for token in tokens:
            
            if (token not in dicionario_set) and (token not in nomes_proprios):
                print(token)
                cont +=1 

        return cont
        
    #66. number of capitalization errors
    def n_capitalization_errors(self):
        
        sentencas = self.sentences()
        
        count = 0

        nomes_proprios = self.nomes_proprios()

        for sent in sentencas:

            for i, token in enumerate(sent):

                if (str(token).islower()):
                    if (i == 0) or (token in nomes_proprios):
                        count += 1
                        print(sent)
                else:
                    if (i != 0):
                        count += 1
                        print(sent)

        return count

    #67. number of punctuation errors
    def n_punctuation_errors(self):

        pass
        #Vírgula;

        #Ponto e vírgula;

        #Ponto final;

        #Ponto de exclamação;

        #Ponto de interrogação;

        #Dois-pontos;

        #Aspas;

        #Travessão;

        #Parênteses.





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
    