import sys
sys.path.insert(0, 'src')

import uol_redacoes_xml
from Texto import Texto
from sklearn.model_selection import train_test_split
from cria_corpus_kaggle import nova_escala
import pandas as pd

def registra_redacao(row, uso_AM):
    obj_txt = Texto(row['texto'], row['avaliacao'], uso_AM, 'uol')
    obj_txt.to_xml()

redacoes = uol_redacoes_xml.load()

textos = [redacao.text for redacao in redacoes]

pontuacoes = [redacao.final_score for redacao in redacoes]
pontuacoes_nova_escala = list(map(lambda x: nova_escala(x, 0, 10, 0, 1000) , pontuacoes))

df_redacoes = pd.DataFrame({'textos': textos, 'avaliacoes' : pontuacoes_nova_escala})

# 25% das redações são de treino
textos_treino, textos_teste, pont_treino, pont_teste = train_test_split(df_redacoes['textos'], df_redacoes['avaliacoes'], test_size=0.25, random_state=500)


df_treino = pd.DataFrame({'texto' : textos_treino, 'avaliacao' : pont_treino})
df_teste = pd.DataFrame({'texto' : textos_teste, 'avaliacao' : pont_teste})

df_treino.apply(lambda x: registra_redacao(x, uso_AM = 'treino'), axis=1)
df_teste.apply(lambda x: registra_redacao(x, uso_AM = 'teste'), axis=1)