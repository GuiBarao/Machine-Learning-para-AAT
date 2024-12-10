import sys

sys.path.insert(0, 'src')

from Texto import Texto
import pandas as pd


def nova_escala(valor, min_original, max_original, min_novo, max_novo):
   return ((valor - min_original)/ (max_original - min_original)) * (max_novo - min_novo) + min_novo

def calcula_pontuacao(linha, peso_regFormal=1, peso_tematica=1, peso_narrativa=1, peso_coesao=1):
    reg_formal = linha['formal_register']
    tematica = linha['thematic_coherence']
    narrativa = linha['narrative_rhetorical_structure']
    coesao = linha['cohesion']

    reg_formalValor = reg_formal * peso_regFormal

    tematicaValor = tematica * peso_tematica

    narrativaValor = narrativa * peso_narrativa

    coesaoValor = coesao * peso_coesao

    sumPontuacoes = sum([reg_formalValor,tematicaValor,narrativaValor,coesaoValor])
    sumPesos = sum([peso_regFormal, peso_tematica, peso_narrativa, peso_coesao])

    pontuacao = sumPontuacoes/ sumPesos

    return round(nova_escala(pontuacao, 1, 5, 0, 1000))

def col_pontuacao(data):
    pontuacao = data.drop(['id','essay','prompt'], axis=1)
    data['pontuacao'] = pontuacao.apply(calcula_pontuacao, axis=1)
    return data

def instancia_linha(row):
    return Texto(row['essay'],row['pontuacao'], row['uso_AM'], 'kaggle')

def elimina_flags(corpus):
    flags = ['[P]', '[ P]', '[p]', '{p}', '[S]', '[s]',
                '[T]', '[t]', '{t}', '{x}', '[R]', '[X]', '[X~]',
                '[r]', '[x]', '[?]', '{?}', '{?]', '[?}', '[LC]',
                '[LT]', '[lt]', '<i>', '<t>', '[s]', '[r]', '<i/>']
    
    textos_sem_flags = []
    for texto in corpus['essay']:
        for flag in flags:
            texto = texto.replace(flag, '')
        
        textos_sem_flags.append(texto)

    novo_corpus = corpus.copy()
    novo_corpus['essay'] = textos_sem_flags

    return novo_corpus
    
def cvs_to_xml():
    raw_teste = pd.read_csv('data/corpus_csv/test.csv')
    raw_treino = pd.read_csv('data/corpus_csv/train.csv')
    raw_validacao = pd.read_csv('data/corpus_csv/validation.csv')

    teste = col_pontuacao(raw_teste)
    treino = col_pontuacao(raw_treino)
    validacao = col_pontuacao(raw_validacao)
    
    teste['uso_AM'] = 'teste'
    treino['uso_AM'] = 'treino'
    validacao['uso_AM'] = 'treino'

    raw_corpus = pd.concat([teste,treino], ignore_index=True)
    raw_corpus = pd.concat([raw_corpus,validacao], ignore_index=True)

    corpus = raw_corpus[['essay', 'pontuacao', 'uso_AM']]

    corpus_sem_flags = elimina_flags(corpus)

    instancias = corpus_sem_flags.apply(instancia_linha, axis=1)
    
    for texto in instancias:
        texto.to_xml()
    
def main():
    cvs_to_xml()

if __name__ == "__main__":
    main()