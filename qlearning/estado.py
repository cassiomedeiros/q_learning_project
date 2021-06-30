
import numpy as np
from typing import Tuple, List

class Estado:
    """Classe responsável por mover o agente dentro do espaço vetorial.
    """
    def __init__(self, estado: Tuple[int, int]=(5, 0)):
        self.estado = estado
        self.entregou_objeto: bool = False
        self.deterministico: bool = True
        self._estados_entrega: List[Tuple[int, int]] = [
            (0, 2), (0, 4), (0, 3)
        ]
        self._estados_bloqueados: List[Tuple[int, int]] = [
            (1, 3), (4, 0), (4, 1), (4, 3), 
            (4, 4), (4, 5), (4, 6), (5, 6)]

    def obter_recompensa(self) -> int:
        """Obtém a recompensa para o estado atual.
        """
        if self.estado in self._estados_entrega:
            return 1
        else:
            return 0

    def entregou(self) -> bool:
        """Verifica se o estado atual é uma posição de entrega.
        """
        if self.estado in self._estados_entrega:
            self.entregou_objeto = True

    def _mover(self, movimento):
        if movimento == "cima":
            return np.random.choice(["cima", "esquerda", "direita"], p=[0.8, 0.1, 0.1])
        if movimento == "baixo":
            return np.random.choice(["baixo", "esquerda", "direita"], p=[0.8, 0.1, 0.1])
        if movimento == "esquerda":
            return np.random.choice(["esquerda", "cima", "baixo"], p=[0.8, 0.1, 0.1])
        if movimento == "direita":
            return np.random.choice(["direita", "cima", "baixo"], p=[0.8, 0.1, 0.1])

    def proximo_movimento(self, movimento):

        if self.deterministico:
            if movimento == "cima":
                proximo_estado = (self.estado[0] - 1, self.estado[1])
            elif movimento == "baixo":
                proximo_estado = (self.estado[0] + 1, self.estado[1])
            elif movimento == "esquerda":
                proximo_estado = (self.estado[0], self.estado[1] - 1)
            else:
                proximo_estado = (self.estado[0], self.estado[1] + 1)
            self.deterministico = False
        else:
            movimento = self._mover(movimento)
            self.deterministico = True
            proximo_estado = self.proximo_movimento(movimento)
        
        if (proximo_estado[0] >= 0) and (proximo_estado[0] <= 5):
            if (proximo_estado[1] >= 0) and (proximo_estado[1] <= 6):
                if proximo_estado not in self._estados_bloqueados:
                    return proximo_estado
        
        return self.estado