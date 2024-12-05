import pandas as pd

corpus = pd.DataFrame()

lista = [('a',1), ('b',2), ('c',3)]

textos = [texto for texto, avaliacao in lista]
avaliacoes = [avaliacao for texto, avaliacao in lista]

corpus = pd.concat([corpus, pd.DataFrame({'texto' : textos, 'avaliacao' : avaliacoes})], ignore_index=True )

print(corpus)