import spacy

nlp = spacy.load("pt_core_news_sm")
frase = "O gato dorme tranquilamente na cama."
doc = nlp(frase)


# Função para calcular a altura
def altura_arvore(doc):
    return max(len(list(token.ancestors)) for token in doc) + 1

altura = altura_arvore(doc)
print(f"Altura da árvore sintática: {altura}")
