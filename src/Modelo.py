import xml.etree.ElementTree as ET
from Texto import Texto
import numpy as np


class Modelo:
    
    diretorio_corpus_kaggle = 'data/corpus_kaggle.xml'
    diretorio_corpus_uol = 'data/corpus_uol.xml'

    def __init__(self, tipo="geral"):
        self.tipo = tipo


    def extrair_sofisticacao_lexica(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.nChar())
                linha.append(txt.nWords())
                linha.append(txt.nLongWords())
                linha.append(txt.nShortWords())
                linha.append(txt.most_frequent_wordLen())
                linha.append(txt.average_wordLen())
                linha.append(txt.nSentences())
                linha.append(txt.nLongSentences())
                linha.append(txt.nShortSentences())
                linha.append(txt.mostFrequent_sentenceLen())
                linha.append(txt.average_sentenceLen())
                linha.append(txt.nUniqueWords())
                linha.append(txt.nStopWords())
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break
 

        header = "nChar,nWords,nLongWords,nShortWords,mostFreqWordLen,avgWordLen," \
        "nSentences,nLongSentences,nShortSentences,mostFreqSentLen,avgSentLen," \
        "nDifferentWords,nStopwords, avaliacao"

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f", header=header)
    
    def extrair_leiturabilidade(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.gunningFog())
                linha.append(txt.flesch_readindEase())
                linha.append(txt.flesch_kincaid())
                linha.append(txt.dale_chall())
                linha.append(txt.automated_readabilityIndex())
                linha.append(txt.simple_gobbledygook())
                linha.append(txt.lix())
                linha.append(txt.word_variationIndex())
                linha.append(txt.nominal_ratio())
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break
 

        header = "gunningFog,flesch_readindEase,flesch_kincaid,dale_chall,automated_readabilityIndex, " \
                    "simple_gobbledygook, lix, word_variationIndex, nominal_ratio, avaliacao"

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f", header=header)

    def extrair_diversidade_lexica(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.typeToken_ratio())
                linha.append(txt.guiraud_index())
                linha.append(txt.yule_K())
                linha.append(txt.hapax_legomena())
                linha.append(txt.advanced_guiraud())
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break
 

        header = "TypeTokenRatio, GuiraudsIndex, Yule's_K, HapaxLegonema, AdvancedGuiraud, Avaliacao"

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f", header=header)

    def extrair_gramatica(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.n_differents_posTags())
                linha.append(txt.height_treeSentence())
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break
 

        header = "nDifferentsPosTags, HeightTreeSentence, Avaliacao"

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f", header=header)

    def extrair_numero_de_cada_pos_tag(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.n_coordinating_conjunction())
                linha.append(txt.n_numeral())
                linha.append(txt.n_determiner())
                linha.append(txt.n_existencial())
                linha.append(txt.n_subordinatingConjunction())
                linha.append(txt.n_adjective())
                linha.append(txt.n_comparativeAdjective())
                linha.append(txt.n_superlativeAdjective())
                linha.append(txt.n_ordinalAdjective_or_numeral())
                linha.append(txt.n_modalAuxiliary())
                linha.append(txt.n_singular_or_massCommun_noun())
                linha.append(txt.n_pluralCommonNoun())
                linha.append(txt.n_preposition())
                linha.append(txt.n_participle())
                linha.append(txt.n_predeterminer())
                linha.append(txt.n_genitiveMarker())
                linha.append(txt.n_personalPronoun())
                linha.append(txt.n_possessivePronoun())
                linha.append(txt.n_adverb())
                linha.append(txt.n_comparativeAdverb())
                linha.append(txt.n_superlativeAdverbs())
                linha.append(txt.n_preposition_or_infinitive())
                linha.append(txt.n_verb_baseForm())
                linha.append(txt.n_verb_pastTense())
                linha.append(txt.n_verb_gerund())
                linha.append(txt.n_verb_pastParticiple())
                linha.append(txt.n_verb_thirdPersonSingPresent())
                linha.append(txt.n_whDeterminer())
                linha.append(txt.n_whAdverb())
                linha.append(txt.n_whPronoun())

                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)
            except:
                break


        header = "coordinating_conjunction, numeral, determiner, existencial, subordinatingConjunction, " \
        "adjective, comparativeAdjective, superlativeAdjective, ordinalAdjective_or_numeral, modalAuxiliary, " \
        "singular_or_massCommun_noun, pluralCommonNoun, preposition, participle, predeterminer, genitiveMarker, " \
        "personalPronoun, possessivePronoun, adverb, comparativeAdverb, superlativeAdverbs, preposition_or_infinitive, " \
        "n_verb_baseForm, n_verb_pastTense, n_verb_gerund, n_verb_pastParticiple, n_verb_thirdPersonSingPresent, " \
        "n_whDeterminer, n_whAdverb, whPronoun"


        np.savetxt( caminho, np.array(atributos),  delimiter=",", header=header, fmt='%d')

    def extrair_mecanica(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.n_speelChecking_errors())
                linha.append(txt.n_capitalization_errors())
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break


 

        header = "n_speelChecking_errors, n_capitalization_errors, Avaliacao"

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f", header=header)

    def extrair_coerencia(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.averageDistance_neighboringPoints(tipo_distancia="cos"))
                linha.append(txt.averageDistance_neighboringPoints(tipo_distancia="euclid"))

                linha.append(txt.minDistance_neighboringPoints(tipo_distancia="cos"))
                linha.append(txt.maxDistance_neighboringPoints(tipo_distancia="cos"))
                linha.append(txt.quotientDistance_neighboringPoints(tipo_distancia="cos"))

                linha.append(txt.minDistance_neighboringPoints(tipo_distancia="euclid"))
                linha.append(txt.maxDistance_neighboringPoints(tipo_distancia="euclid"))
                linha.append(txt.quotientDistance_neighboringPoints(tipo_distancia="euclid"))


                linha.append(txt.averageDistance_anyTwoPoints(tipo_distancia="cos"))
                linha.append(txt.averageDistance_anyTwoPoints(tipo_distancia="euclid"))


                linha.append(txt.maxDifference_anyTwoPoints(tipo_distancia="cos"))
                linha.append(txt.maxDifference_anyTwoPoints(tipo_distancia="euclid"))


                linha.append(txt.clarkEvan_distance_nearestNeighbor(tipo_distancia="cos"))
                linha.append(txt.clarkEvan_distance_nearestNeighbor(tipo_distancia="euclid"))

                linha.append(txt.average_distance_nearestNeighbor(tipo_distancia="cos"))
                linha.append(txt.average_distance_nearestNeighbor(tipo_distancia="euclid"))

                linha.append(txt.cumulative_frequency_distribution(tipo_distancia="cos"))
                linha.append(txt.cumulative_frequency_distribution(tipo_distancia="euclid"))

           
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)
            except:
                break

        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f")

    def extrair_dadosEspaciais(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.averageEuclideanDistance_betweenCentroidAndEachPoint())

                linha.append(txt.minimalEuclideanDistance_betweenCentroidAndEachPoint())
                linha.append(txt.maximalEuclideanDistance_betweenCentroidAndEachPoint())
                linha.append(txt.coefficientEuclideanDistance_betweenCentroidAndEachPoint())

                linha.append(txt.standard_distance())
                linha.append(txt.relative_distance())
                linha.append(txt.determinant_distance_matrix())
                
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)

            except:
                break


 
        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f")

    def extrair_autocorrelacaoEspacial(self, caminho, corpus):
        id = 0

        atributos = []
        
        while(True):
            try:
                print(id)
                txt = Modelo.xml_to_object(id, corpus)

                linha = []

                linha.append(txt.morans_I())
                linha.append(txt.gettis_G())
                linha.append(txt.gearys_C())
                
                linha.append(float(txt.avaliacao))

                id += 1

                atributos.append(linha)
             

            except:
                break


 
        np.savetxt( caminho, np.array(atributos),  delimiter=",", fmt="%.5f")

    def extrair_geral (self, tipos, corpus):

        array_geral = None

        y_array_geral = None

        for tipo in tipos:
            array = np.loadtxt(f"data/atributos/{corpus}/{tipo}.csv", delimiter=",")
            x = array[:, :-1]  

            if array_geral is None:
                array_geral = x
            else:
                array_geral = np.hstack((array_geral, x))

            if(y_array_geral is None):
                y_array_geral =  array[:, -1]  


        y_array_geral = y_array_geral.reshape(-1, 1)
        array_geral = np.hstack((array_geral, y_array_geral))
        np.savetxt(f"data/atributos/{corpus}/geral.csv", array_geral,  delimiter=",", fmt="%.5f")


        


    @staticmethod
    def diretorio_corpus(corpus):

        if corpus == 'uol':
            diretorio = Modelo.diretorio_corpus_uol
        elif corpus == 'kaggle':
            diretorio = Modelo.diretorio_corpus_kaggle
        else:
            exit()

        return diretorio

    #Transforma um objeto em xml e salva no arquivo corpus.xml
    def to_xml(self):

        caminho_corpus = Modelo.diretorio_corpus(self.corpus)

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
        caminho_corpus = Modelo.diretorio_corpus(corpus)
        
        texto = Modelo.buscar_texto(id, caminho_corpus)

        if (texto):
            return Texto(texto.find('redacao').text, texto.find('avaliacao').text, texto.find('uso_AM').text, texto.find('corpus').text)
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