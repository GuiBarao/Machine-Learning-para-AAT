import numpy as np
from sklearn.model_selection import train_test_split
import joblib
from fpdf import FPDF


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
    pdf.cell(50, 10, "Avaliador Humano", border=1, align="C")
    pdf.cell(50, 10, "Avaliacao Sistema", border=1, align="C")
    pdf.ln()

    # dados
    pdf.set_font("Arial", size=12)
    for humano, sistema in dados:
        pdf.cell(50, 10, str(humano), border=1, align="C")
        pdf.cell(50, 10, str(sistema), border=1, align="C")
        pdf.ln()

    pdf.output(nome_arquivo)
    print(f"PDF salvo como {nome_arquivo}")

def comparativo_humano_sistema(corpus):
    extratos = divisao_features(f"data\\atributos\\{corpus}\\geral.csv")
    x_teste = extratos[1]
    y_teste = extratos[3] #lista de avaliações dos avaliadores humanos

    modelo = joblib.load(f"modelos_treinados\\{corpus}\\geral.pkl")
    predicoes = modelo.predict(x_teste) #lista de avaliações do sistema

    dados_tabela = [(y_teste[i], predicoes[i])  for i in range(len(predicoes))]

    cria_tabela(dados_tabela, f"comparativo_geral_{corpus}.pdf")

def main():
    comparativo_humano_sistema("kaggle")


    
    
if __name__ == "__main__":
    main()