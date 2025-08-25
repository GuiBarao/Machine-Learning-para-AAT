import numpy as np

INTERVALO_MEDIOS = (301, 400)
INTERVALO_ALTOS  = (401, 500)

def load_csv(path):
    try:
        return np.loadtxt(path, delimiter=",")
    except ValueError:
        return np.loadtxt(path, delimiter=",", skiprows=1)

def igualar_intervalos(caminho_in, caminho_out, seed=317):
    data = load_csv(caminho_in)
    y = data[:, -1]

    idx_medios = np.where((y >= INTERVALO_MEDIOS[0]) & (y <= INTERVALO_MEDIOS[1]))[0]
    idx_altos  = np.where((y >= INTERVALO_ALTOS[0]) & (y <= INTERVALO_ALTOS[1]))[0]

    n_medios = len(idx_medios)
    n_altos  = len(idx_altos)

    remover = max(0, n_medios - n_altos)  # só remove se médios > altos

    mask = np.ones(len(data), dtype=bool)
    if remover > 0 and n_medios > 0:
        rng = np.random.default_rng(seed)
        remove_idx = rng.choice(idx_medios, size=remover, replace=False)
        mask[remove_idx] = False

    data_filtrado = data[mask]
    np.savetxt(caminho_out, data_filtrado, delimiter=",", fmt="%.5f")

    print(
        f"Médios (301–400): {n_medios} → {n_medios-remover} | "
        f"Altos (401–500): {n_altos} | "
        f"Salvo em: {caminho_out} ({len(data_filtrado)} linhas)"
    )

# uso
igualar_intervalos(
    r"testaNovoModelo\atributos\kaggle\geralFiltrado.csv",
    r"testaNovoModelo\atributos\kaggle\geralFiltrado.csv"
)
