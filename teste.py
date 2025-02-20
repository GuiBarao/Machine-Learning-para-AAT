import spacy


txt = 'Eu tenho duas casas.'

pln = spacy.load("pt_core_news_lg")

tokens = pln(txt)

for token in tokens:
    
        print(f'{token.text} // {token.pos_} // {token.tag_} // {token.morph} // {token.dep_} // {token.lemma_}')
