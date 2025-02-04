import spacy


txt = 'Isso pode ser raríssimo'

pln = spacy.load("pt_core_news_lg")

tokens = pln(txt)

for token in tokens:

    print(f'{token.text} // {token.pos_} // {token.morph} // {token.dep_}')
