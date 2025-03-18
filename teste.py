import spacy

txt = '''Possui graduação em Ciência da Computação pela 
Universidade Estadual de Campinas (1999), mestrado
em Ciência da Computação pela Universidade Estadual
de Campinas (2003) e doutorado em Ciência da Computação
pela Universidade Estadual de Campinas (2012). Atualmente
é professor de ensino superior nível IV da Universidade 
Estadual de Mato Grosso do Sul. Tem grande experiência e
conhecimento nas seguintes áreas da computação: aprendizagem
de máquina, reconhecimento de padrões, mineração de dados
, informática na educação, agentes de interface, ambientes
de educação a distância, educação a distância e interfaces
homem-máquina.'''

pln = spacy.load("pt_core_news_lg")

doc = pln(txt)

for sent in doc.sents:
    for token in sent:
        print("-----",token.text, "------")
