import pandas as pd
import matplotlib.pyplot as plt

from qlearning.estado import Estado
from qlearning.agente import Agente

if __name__ == "__main__":

    agente = Agente(
        taxa_aprendizado=0.2,
        taxa_exploracao=0.2,
        decaimento_gama=0.9
    )
    
    agente.executar(100, verbose=False)

    ax = pd.DataFrame(agente.resumo).set_index('episodio').plot(kind='line', figsize=(16,6))
    ax.set_title('Episódios x passos')
    ax.get_legend().remove()
    ax.set_ylabel("Passos")
    ax.set_xlabel('Episódios')
    plt.box(False)
    plt.savefig('./report/resultado.png')