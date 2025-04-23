import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import math
import spacy
import syllapy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from scipy.spatial.distance import pdist, squareform


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
        
        if len(sentenca_aux) != 0 : 
            sentencas.append(sentenca_aux)

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

        return 0 if denominador == 0 else numerador / denominador
        

    def n_substantivos(self):
        return self.count_of_tag("NOUN")

    def n_pronomes(self):
        return self.count_of_tag("PRON")
    
    def n_verbos(self):
        return self.count_of_tag("VERB")
    
    #22. nominal ratio
    def nominal_ratio(self):
        substantivos = self.n_substantivos()
        preposicoes = self.n_preposition()
        participios = self.n_participle()
        pronomes = self.n_pronomes()
        adverbios = self.n_adverb()
        verbos = self.n_verbos()

        try:
            return (substantivos + preposicoes + participios) / (pronomes + adverbios + verbos)
        except:
            return 0

    #23. type-token-ratio
    def typeToken_ratio(self):
            return self.nWords() / self.nWordTypes()
    
    #24. Guiraud’s index
    def guiraud_index(self):
        return self.nWordTypes() / math.sqrt(self.nWords())
    
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
    
    #30. height of the tree presenting sentence structure
    def height_treeSentence(self):
        doc = Texto.pln(self.redacao)
        somaAlturas = 0

        for sentenca in doc.sents:

            n_antecessores = [len(list(token.ancestors)) for token in sentenca]
            
            somaAlturas += max(n_antecessores) + 1
            

        return somaAlturas





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

    
    #37. preposition/subordinating conjunction 
    def n_subordinatingConjunction(self):
        return self.count_of_tag("SCONJ")
    
    #38. adjective
    def n_adjective(self):
        return self.count_of_tag("ADJ")


    @staticmethod
    def adj_compIgualdade(tokenAnterior, tokenPosterior):
        igualdade_adv1 = ['tão', 'quão', 'assim', 'tanto', 'quase', 'exatamente', 'igualmente']

        igualdade_adv2 = ['quanto', 'como', 'que']

        return (tokenAnterior.lower() in igualdade_adv1) and (tokenPosterior.lower() in igualdade_adv2)

    @staticmethod
    def adj_compSuperioridade(tokenAnterior, token):
        irregulares = ['melhor', 'pior', 'maior', 'menor', 'superior', 'inferior']

        return tokenAnterior == 'mais' or token.lower() in irregulares

    @staticmethod
    def adj_compInferioridade(tokenAnterior):
        return (tokenAnterior.lower() == "menos")

    #39. comparative adjective
    def n_comparativeAdjective(self):

        tokens = Texto.pln(self.redacao)
        
        count = 0
        
        for i, token in enumerate(tokens):

            if (token.pos_ != 'ADJ') or (i == 0) or (i == len(tokens) -1):
                continue

            tokenAnterior = tokens[i-1]
            tokenPosterior = tokens[i+1]


            if (Texto.adj_compIgualdade(tokenAnterior.text, tokenPosterior.text)):
                count += 1

            elif (Texto.adj_compSuperioridade(tokenAnterior.text, token.text)):
                count += 1

            elif (Texto.adj_compInferioridade(tokenAnterior.text)):
                count += 1


        return count

    #40. superlative adjective
    def n_superlativeAdjective(self):
        sufixos = ['íssimo', 'íssima', 'íssimos', 'íssimas', 
            'érrimo', 'érrima', 'érrimos', 'érrimas',
            'ílimo', 'ílima', 'ílimo']

        tokens = self.tokenizado_pos()

        count = 0

        for token, tag in tokens:
            if(tag == "ADJ") and (token.lower() in sufixos):
                count += 1 

        return count


    #41. ordinal adjective or numeral
    def n_ordinalAdjective_or_numeral(self):

        tokens = Texto.pln(self.redacao)

        count = 0

        for token in tokens:

            if "NumType=" in str(token.morph):
                count += 1

        return count
    
    #42. modal auxiliary
    def n_modalAuxiliary(self):

        tokens = Texto.pln(self.redacao)

        modais_lista = ["dever", "ter", "precisar", "haver", "poder", "conseguir",
                        "saber", "querer", "pretender", "convém"]
        
        return len([token.text for token in tokens if token.lemma_.lower() in modais_lista])
    
    #43. singular or mass common noun
    def n_singular_or_massCommun_noun(self):
        nomesProprios = self.nomes_proprios()

        tokensPos = self.tokenizado_pos()

        count = 0

        for token, tag in tokensPos:
            if tag == 'NOUN' and token.lower() not in nomesProprios:
                count += 1

        return count
    
    #44. plural common noun
    def n_pluralCommonNoun(self):

        tokens = Texto.pln(self.redacao)

        nomesProprios = self.nomes_proprios()

        count = 0

        for token in tokens:
            if token.pos_ == 'NOUN' and 'Plur' in str(token.morph) and token.text not in nomesProprios:
                count += 1
        
        return count

    #45. singular proper noun
    def n_singularProperNoun(self):
        tokens = Texto.pln(self.redacao)

        nomesProprios = self.nomes_proprios()

        count = 0
        for token in tokens:
            if token.text in nomesProprios and 'Plur' not in str(token.morph):
                count += 1

        return count
    
    #46. plural proper noun
    def n_pluralProperNoun(self):
        tokens = Texto.pln(self.redacao)

        nomesProprios = self.nomes_proprios()

        count = 0
        for token in tokens:
            if token.text in nomesProprios and 'Plur' in str(token.morph):
                count += 1

        return count
    
    #47. preposition
    def n_preposition(self):
        return self.count_of_tag("ADP")
    
    #48. participle
    def n_participle(self):

        tokens = Texto.pln(self.redacao)

        count = 0
        for token in tokens:
            if token.pos_ == 'VERB' and 'VerbForm=Part' in str(token.morph):
                count += 1

        return count
    

    #49. predeterminer
    def n_predeterminer(self):
        tokens = self.tokenizado_pos()

        count = 0
        tagAnterior = None

        for _, tag in tokens:

            if(tag == 'DET') and (tagAnterior == 'DET'):
                count += 1

            tagAnterior = tag  

        return count
    
    #50. genitive marker
    def n_genitiveMarker(self):
        tokens = Texto.pln(self.redacao)

        genitives = ["de", "do", "da", "dos", "das"]

        count = 0
        for token in tokens:
            if token.dep_ == 'case' and token.text.lower() in genitives:
                count += 1
        
        return count
    
    #51. personal pronoun
    def n_personalPronoun(self):
        return self.count_of_tag("PRON")
    
    #52. possessive pronoun
    def n_possessivePronoun(self):
        pronomesPossesivos = ["meu", "minha", "meus", "minhas", "teu", "tua", "teus", "tuas",
        "seu", "sua", "seus", "suas", "nosso", "nossa", "nossos", "nossas",
            "vosso", "vossa", "vossos", "vossas"]
        
        tokens = self.tokenizado(exclui_especiais=True, lower=True)

        count = 0

        for token in tokens:
            if token in pronomesPossesivos:
                count += 1

        return count

    #53. adverb
    def n_adverb(self):
        return self.count_of_tag("ADV")
    
    #54. comparative adverb
    def n_comparativeAdverb(self):
        termosRegulares = ['mais', 'menos']
        termosIrregulares = ['mais', 'menos', 'melhor', 'pior']

        tokensPos = self.tokenizado_pos()

        tokenAnterior = None
        count = 0

        for token, tag in tokensPos:

            if tag == 'ADV' and tokenAnterior in termosRegulares:
                count += 1
                continue
            elif tag == 'ADV' and token.lower() in termosIrregulares:
                count+=1
            
            tokenAnterior = token.lower()

        return count
    

    #55. superlative adverb
    def n_superlativeAdverbs(self):
        sufixos = ['íssimo', 'íssima', 'íssimos', 'íssimas', 
            'érrimo', 'érrima', 'érrimos', 'érrimas',
            'ílimo', 'ílima', 'ílimo']

        tokens = self.tokenizado_pos()

        count = 0

        for token, tag in tokens:
            if(tag == "ADV") and (token.lower() in sufixos):
                count += 1 

        return count

    #56. particle, “to” as preposition or infinitive marker
    def n_preposition_or_infinitive(self):
        preposicoes = ["para", "a", "até", "na", "no"]

        tokens = Texto.pln(self.redacao)
        count = 0

        for token in tokens:

            if('VerbForm=Inf' in token.morph):
                count += 1
                continue

            if(token.pos_ == 'ADP') and (token.text.lower() in preposicoes):
                count += 1


        return count
            
    #57. verb - base form
    def n_verb_baseForm(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        for token in tokens:

            if('VerbForm=Inf' in token.morph):
                count += 1


        return count

    #58. verb - past tense
    def n_verb_pastTense(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        pos_verbs = ['VERB', 'AUX']

        for token in tokens:

            if (token.pos_ in pos_verbs) and ('Tense=Past' in token.morph):
                count += 1


        return count

    #59. verb - gerund/present participle 
    def n_verb_gerund(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        pos_verbs = ['VERB', 'AUX']

        for token in tokens:

            if (token.pos_ in pos_verbs) and ('VerbForm=Ger' in token.morph):
                count += 1
                
        return count

    #60. verb - past participle
    def n_verb_pastParticiple(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        pos_verbs = ['VERB', 'AUX']

        for token in tokens:

            if (token.pos_ in pos_verbs) and ('VerbForm=Part' in token.morph):
                count += 1


        return count

    #61. verb - 3rd person sing. present
    def n_verb_thirdPersonSingPresent(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        pos_verbs = ['VERB', 'AUX']

        for token in tokens:

            if (token.pos_ in pos_verbs) and ('Number=Sing' in token.morph) and ('Person=3' in token.morph) and ('Tense=Pres' in token.morph):
                count += 1

        return count
    
    #62. wh-determiner
    def n_whDeterminer(self):
        tokens = Texto.pln(self.redacao)
        count = 0

        whDeterminers = ["que", "qual", "quais"]

        for token in tokens:

            if token.pos_ == 'DET' and token.text.lower() in whDeterminers:
                count += 1

        return count

    #63. wh-pronoun
    def n_whPronoun(self):
        tokens = self.tokenizado(lower=True)
        count = 0

        whPronouns = ['quem', 'que', 'qual', 'quais']

        for token in tokens:
            if token in whPronouns:
                count += 1

        return count
    
    #64. wh-adverb
    def n_whAdverb(self):
        whAdverbs = ["quando", "onde", "aonde", "donde", "porque", "como", "quão"]

        tokens = self.tokenizado(lower=True)
        count = 0
        for i, token in enumerate(tokens):

            if token in whAdverbs:
                count += 1
            elif i != 0 and token == 'que' and tokens[i-1] == 'por':
                count += 1 

        return count


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
                else:
                    if (i != 0):
                        count += 1

        return count


    
    #Atributos de distância (Cos e Euclid)

    def janelas_deslizantes(self):
        
        tokens = self.tokenizado()


        tam_janela = int(len(tokens) * 0.25) + 1
        tam_janela = max(tam_janela, 1)

        #   25          = 10
        #   tam_janela  = passo
        passo = math.ceil((tam_janela*10)/25)

        janelas = []

        inicio = 0 
        
        fim = tam_janela

        while(fim <= len(tokens)):

            janelas.append(tokens[inicio : fim])
            
            inicio += passo
            fim += passo

            if (fim > len(tokens)):

                fim = len(tokens)
                janelas.append(tokens[inicio : fim])
                break
        
        janelas_strings = [' '.join(janela) for janela in janelas]

        return janelas_strings

    def similaridade_cosseno(self, texto1, texto2):
        vetorizador = TfidfVectorizer()
        try:
            matriz = vetorizador.fit_transform([texto1,texto2])
        except(ValueError):
            return None
        similaridade = cosine_similarity(matriz[0:1], matriz[1:2])
        return float(similaridade[0][0])

    def distancia_euclid(self, texto1, texto2):
        vetorizador = TfidfVectorizer()
        try:
            matriz = vetorizador.fit_transform([texto1,texto2])
        except(ValueError):
            return None
        distancias = euclidean_distances(matriz[0:1], matriz[1:2])
        return float(distancias[0][0])



    def distancias_pontosVizinhos(self, tipo_distancia = "cos"):
        distancias = []
        janelas = self.janelas_deslizantes()

        for i, janela in enumerate(janelas):

            if(i == 0):
                continue
            
            if(tipo_distancia == "cos"):
                similaridade = self.similaridade_cosseno(janelas[i-1], janela)
                
                if(similaridade): 
                    distancia = 1 - similaridade
                else:
                    distancia = 0

            elif(tipo_distancia == "euclid"):
                distancia = self.distancia_euclid(janelas[i-1], janela)
                if(not distancia): 
                    distancia = 0


            else:
                raise ValueError

            distancias.append(distancia)

        return distancias
    
    #73. average distance between neighboring points, Cos / Euclid
    def averageDistance_neighboringPoints(self, tipo_distancia = "cos"):
        distancias = self.distancias_pontosVizinhos(tipo_distancia= tipo_distancia)
        return sum(distancias)/len(distancias)
    


    #74. minimum and maximum distance between neighboring points and their quotient
    def minDistance_neighboringPoints(self, tipo_distancia = "cos"):
        distancias = self.distancias_pontosVizinhos(tipo_distancia=tipo_distancia)
        return min(distancias)
    
    #74. minimum and maximum distance between neighboring points and their quotient
    def maxDistance_neighboringPoints(self, tipo_distancia = "cos"):
        distancias = self.distancias_pontosVizinhos(tipo_distancia=tipo_distancia)
        return max(distancias)
    
    #74. minimum and maximum distance between neighboring points and their quotient
    def quotientDistance_neighboringPoints(self, tipo_distancia = "cos"):
        menor = self.minDistance_neighboringPoints(tipo_distancia=tipo_distancia)
        maior = self.maxDistance_neighboringPoints(tipo_distancia=tipo_distancia)

        if(menor == 0):
            return 0

        return maior/menor
    


    def distancias_qualquerPontos(self, tipo_distancia = "cos"):

        janelas = self.janelas_deslizantes()

        distancias = []

        for i, janela in enumerate(janelas):

            for j in range(i+1, len(janelas)):

                if(tipo_distancia == "cos"):
                    similaridade = (self.similaridade_cosseno(janela, janelas[j]))
                    if(similaridade): 
                        distancia = 1 - similaridade
                    else:
                        distancia = 0

                elif(tipo_distancia == "euclid"):
                    distancia = self.distancia_euclid(janela, janelas[j])
                    if(not distancia): 
                        distancia = 0
                
                else:
                    raise ValueError
                
                distancias.append(distancia)

        return distancias

    #75. average distance between any two points
    def averageDistance_anyTwoPoints(self, tipo_distancia = "cos"):
        distancias = self.distancias_qualquerPontos(tipo_distancia=tipo_distancia)
        return sum(distancias) / len(distancias)
    
    

    #76. maximum difference between any two points
    def maxDifference_anyTwoPoints(self, tipo_distancia = "cos"):
        distancias = self.distancias_qualquerPontos(tipo_distancia=tipo_distancia)
        return max(distancias)
    

    def distances_nearestNeighbors(self, tipo_distancia = "cos"):

        if tipo_distancia == "cos":
            distancias = self.distancias_pontosVizinhos(tipo_distancia=tipo_distancia)
        elif tipo_distancia == "euclid": 
            distancias = self.distancias_pontosVizinhos(tipo_distancia=tipo_distancia)
        else:
            raise ValueError
        
        distancia_primeiros_vizinhos = distancias[0]
        distancia_ultimos_vizinhos = distancias[-1]

        vizinhos_maisProximos = [distancia_primeiros_vizinhos, distancia_ultimos_vizinhos]

        for i, distancia in enumerate(distancias):
            
            if (i == len(distancias) -1 ):
                continue

            if (distancia < distancias[i+1]):
                vizinhos_maisProximos.append(distancia)
            else:
                vizinhos_maisProximos.append(distancias[i+1])
        
        return vizinhos_maisProximos

         
    #77. Clark and Evan’s distance to the nearest neighbor
    def clarkEvan_distance_nearestNeighbor(self, tipo_distancia = "cos"):
        r = self.distances_nearestNeighbors(tipo_distancia=tipo_distancia)

        N = len(self.janelas_deslizantes())
        
        somatorio = 0
        for i in range(N):
            somatorio += r[i]

        return somatorio / (N / (1 / (2 * math.sqrt(N))))




    #78. average distance to the nearest neighbor
    def average_distance_nearestNeighbor(self, tipo_distancia = "cos"):
        vizinhos_mais_proximos = self.distances_nearestNeighbors(tipo_distancia=tipo_distancia)

        return sum(vizinhos_mais_proximos)/len(vizinhos_mais_proximos)
            

    #79. cumulative frequency distribution
    def cumulative_frequency_distribution(self, tipo_distancia = "cos"):
        distancia_media = self.average_distance_nearestNeighbor(tipo_distancia = tipo_distancia)
        distancias_vizinhos_mais_proximos = self.distances_nearestNeighbors(tipo_distancia = tipo_distancia)

        cont = 0
        
        for distancia in distancias_vizinhos_mais_proximos:

        

            if distancia <= distancia_media:
                
                cont += 1

        return cont / len(distancias_vizinhos_mais_proximos)

    def centroid_index(self):
        janelas = self.janelas_deslizantes()
        indice_centroid = int(len(janelas) / 2)

        if(len(janelas) % 2 != 0):
            indice_centroid += 1

        return indice_centroid

        
    def distanceBetween_eachPoint_andCentroid (self, tipo_distancia="euclid"):
        
        janelas = self.janelas_deslizantes()
        indexCentroid = self.centroid_index()

        centroid = janelas[indexCentroid]
        

        distancias = []
        
        for i, janela in enumerate(janelas):

            if i == indexCentroid:
                continue

            distancia = self.distancia_euclid(centroid, janela)
            if(not distancia):
                distancia = 0

            distancias.append(distancia)


        return distancias


    #81. average Euclidean distance between the centroid and each point
    def averageEuclideanDistance_betweenCentroidAndEachPoint(self):
        distancias_anyPoint_centroid = self.distanceBetween_eachPoint_andCentroid()
        return sum(distancias_anyPoint_centroid)/len(distancias_anyPoint_centroid)

    
    #82. Minimal and maximal Euclidean distance between the centroid and each point and their coefficient
    def minimalEuclideanDistance_betweenCentroidAndEachPoint(self):
        distancias = self.distanceBetween_eachPoint_andCentroid()
        return min(distancias)    
    
    #82. Minimal and maximal Euclidean distance between the centroid and each point and their coefficient
    def maximalEuclideanDistance_betweenCentroidAndEachPoint(self):
        distancias = self.distanceBetween_eachPoint_andCentroid()
        return max(distancias)  
    
    #82. Minimal and maximal Euclidean distance between the centroid and each point and their coefficient
    def coefficientEuclideanDistance_betweenCentroidAndEachPoint(self):
        min = self.minimalEuclideanDistance_betweenCentroidAndEachPoint()
        max = self.maximalEuclideanDistance_betweenCentroidAndEachPoint()

        if(not min):
           return 0

        return max/min
    
    #83. standard distance
    def standard_distance(self):
        janelas = self.janelas_deslizantes()
        N = len(janelas)
        
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform(janelas).toarray() 

        centroide = np.mean(matriz, axis=0)                    
        distancias = np.linalg.norm(matriz - centroide, axis=1)  
        sd = np.sqrt(np.sum(distancias ** 2) / N)

        return sd
    
    #84. relative distance
    def relative_distance(self):
        dMax = self.maximalEuclideanDistance_betweenCentroidAndEachPoint()
        sd = self.standard_distance()

        return sd/dMax; 


    #85. the determinant of the distance matrix.
    def determinant_distance_matrix(self):
        janelas = self.janelas_deslizantes()
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform(janelas).toarray()

        dist_matrix = squareform(pdist(matriz, metric='euclidean'))

        det = np.abs(np.linalg.det(dist_matrix))

        return det   
      

    #86. Moran’s I
    def morans_I (self) :
        janelas = self.janelas_deslizantes()
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform(janelas).toarray()
        N, n = matriz.shape
        centroide = np.mean(matriz, axis=0)

        W = np.zeros((N, N))
        for i in range(N):
            if i > 0: W[i, i-1] = 1
            if i < N - 1: W[i, i+1] = 1
        S = np.sum(W)

        numerador_total = 0
        for k in range(n):
            Dk = matriz[:, k]
            Dk_c = centroide[k]

            num_k = np.sum([W[i, j] * (Dk[i] - Dk_c) * (Dk[j] - Dk_c)
                            for i in range(N) for j in range(N)])
            den_k = np.sum((Dk - Dk_c) ** 2)

            if den_k != 0:
                numerador_total += num_k / den_k

            return (N / S) * (1 / n) * numerador_total



    #87. Geary’s C
    def gearys_C(self):
        janelas = self.janelas_deslizantes()
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform(janelas).toarray()
        N, n = matriz.shape
        centroide = np.mean(matriz, axis=0)


        W = np.zeros((N, N))
        for i in range(N):
            if i > 0: W[i, i-1] = 1
            if i < N - 1: W[i, i+1] = 1
        S = np.sum(W)

        numerador_total = 0
        for k in range(n):
            Dk = matriz[:, k]
            Dk_c = centroide[k]

            num_k = np.sum([W[i, j] * (Dk[i] - Dk[j]) ** 2
                            for i in range(N) for j in range(N)])
            den_k = np.sum((Dk - Dk_c) ** 2)

            if den_k != 0:
                numerador_total += num_k / den_k

        return ((N - 1) / (2 * S)) * (1 / n) * numerador_total


    #88. Gettis’s G
    def gettis_G(self):
        janelas = self.janelas_deslizantes()
        vetorizador = TfidfVectorizer()
        matriz = vetorizador.fit_transform(janelas).toarray()
        N, n = matriz.shape

       
        W = np.zeros((N, N))
        for i in range(N):
            if i > 0: W[i, i-1] = 1
            if i < N - 1: W[i, i+1] = 1

        soma_G = 0
        for k in range(n):
            Dk = matriz[:, k]
            numerador = np.sum([W[i, j] * Dk[j] for i in range(N) for j in range(N)])
            denominador = np.sum(Dk)

            if denominador != 0:
                soma_G += numerador / denominador

        return soma_G / n




