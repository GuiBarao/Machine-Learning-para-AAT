import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import cohen_kappa_score
import joblib
from fpdf import FPDF
from typing import Tuple, List


def divisao_features(caminho_csv):

    array = np.loadtxt(caminho_csv, delimiter=",")

    #remove a coluna de avaliação (ultima)  
    x = array[:, :-1]
    y = array[:, -1]    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=62)

    return (x_train, x_test, y_train, y_test)

def cria_tabela(dados, nome_arquivo):

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    #titulo
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Comparativo: Avaliador Humano x Sistema", ln=True, align="C")
    pdf.ln(5)

    # header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Indice", border=1, align="C")
    pdf.cell(50, 10, "Avaliador Humano", border=1, align="C")
    pdf.cell(50, 10, "Avaliação Sistema", border=1, align="C")
    pdf.ln()

    # dados
    pdf.set_font("Arial", size=12)
    for i, humano, sistema in dados:
        pdf.cell(50, 10, str(i), border=1, align="C")
        pdf.cell(50, 10, str(humano), border=1, align="C")
        pdf.cell(50, 10, str(sistema), border=1, align="C")
        pdf.ln()

    pdf.output(nome_arquivo)
    print(f"PDF salvo como {nome_arquivo}")

def comparativo_humano_sistema(corpus):
    humanas, sistema = lista_avaliacoes(corpus)

    dados_tabela = [(i, humanas[i], sistema[i])  for i in range(len(sistema))]

    cria_tabela(dados_tabela, f"tabelas\\pdfs\\comparativo_geral_{corpus}.pdf")

def lista_avaliacoes(corpus):
    extratos = divisao_features(f"testaNovoModelo\\atributos\\{corpus}\\geralFiltrado.csv")
    x_teste = extratos[1]
    avaliacoes_humanas = extratos[3] #lista de avaliações dos avaliadores humanos

    modelo = joblib.load(f"testaNovoModelo\\{corpus}\\geral.pkl")
    avaliacoes_sistema = modelo.predict(x_teste) #lista de avaliações do sistema

    avaliacoes_humanas = [int(avaliacoes_humanas[i]) for i in range(len(avaliacoes_humanas))]
    avaliacoes_sistema = [int(avaliacoes_sistema[i]) for i in range(len(avaliacoes_sistema))]

    return (avaliacoes_humanas, avaliacoes_sistema)

def kappa_quadratico(corpus):

    humanas, sistema = lista_avaliacoes(corpus)

    resultado = cohen_kappa_score(humanas, sistema, weights='quadratic')

    return resultado

def porcentagem_avaliacoes_intervalo(lista_avaliacoes: List, intervalo: Tuple[int, int]) -> int:
    
    quantidadeAvaliacoes = len([avaliacao for avaliacao in lista_avaliacoes 
            if avaliacao >= intervalo[0] and avaliacao <= intervalo[1]])
    
    totalAvaliacoes = len(lista_avaliacoes)
    
    return (quantidadeAvaliacoes * 100) / totalAvaliacoes

def testeProporcao():
    humanosUOL, sistemaUOL = lista_avaliacoes("uol")
    humanosKaggle, sistemaKaggle = lista_avaliacoes("kaggle")

    intervalosTeste = {"baixas":(0,400), "medias":(401,700), "altas":(701,1000)}

    return {"uol": [porcentagem_avaliacoes_intervalo(sistemaUOL, intervalosTeste["baixas"]),
                                porcentagem_avaliacoes_intervalo(sistemaUOL, intervalosTeste["medias"]),
                                porcentagem_avaliacoes_intervalo(sistemaUOL, intervalosTeste["altas"])],

                    "kaggle": [porcentagem_avaliacoes_intervalo(sistemaKaggle, intervalosTeste["baixas"]),
                                   porcentagem_avaliacoes_intervalo(sistemaKaggle, intervalosTeste["medias"]),
                                   porcentagem_avaliacoes_intervalo(sistemaKaggle, intervalosTeste["altas"])]}

def main():

    proporcoes = testeProporcao()

    print(proporcoes["kaggle"])


    
    
if __name__ == "__main__":
    main()