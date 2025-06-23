import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import joblib

def arvore(corpus):
    modelo = joblib.load(f"modelos_treinados\\{corpus}\\mecanica.pkl")
    plt.figure(figsize=(100, 80))  
    plot_tree(
        modelo.estimators_[0],
        filled=True,
        fontsize=16  
    )
    plt.tight_layout()

    plt.savefig(f"analise\\arvores\\{corpus}.pdf",format="pdf")

def main():
    arvore("uol")

if __name__ == "__main__":
    main()