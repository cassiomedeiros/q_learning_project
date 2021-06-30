import numpy as np
from typing import Tuple, List, Dict
from qlearning.estado import Estado

class Agente:
    
    """Classe reponsável por controlar o agente a atingir o seu objetivo.
    """

    def __init__(
        self,
        taxa_aprendizado: float = 0.3,
        taxa_exploracao: float = 0.3,
        decaimento_gama: float = 0.8
    ) -> None:
        self.estados: List[Estado] = []
        self.movimentos = ["cima", "baixo", "esquerda", "direita"]
        self.estado = Estado()
        self.entregou = self.estado.entregou
        self.taxa_aprendizado = taxa_aprendizado
        self.taxa_exploracao = taxa_exploracao
        self.decaimento_gama = decaimento_gama
        self.resumo: List[Tuple[int, int]] = list()
        self.agarrou_objeto: bool = False

        self.tabela_q: Dict[Tuple[int, int], dict] = {}
        for i in range(6):
            for j in range(7):
                self.tabela_q[(i, j)] = {}
                for m in self.movimentos:
                    self.tabela_q[(i, j)][m] = (0, False)

    def _escolher_movimento(self) -> str:
        """Obtém movimento com maior recompensa esperada.
        """
        recompensa_maxima: int = 0
        movimento: str = ""

        if np.random.uniform(0, 1) <= self.taxa_exploracao:
            movimento = np.random.choice(self.movimentos)
        else:
            for m in self.movimentos:
                estado_atual = self.estado.estado
                proxima_recompensa = self.tabela_q[estado_atual][m][0]
                if proxima_recompensa >= recompensa_maxima:
                    movimento = m
                    recompensa_maxima = proxima_recompensa
        return movimento

    def _realizar_movimento(self, movimento) -> Estado:
        """Realiza movimento e atualiza o estado.
        """
        estado = self.estado.proximo_movimento(movimento)
        return Estado(estado=estado)

    def _reiniciar_estados(self) -> None:
        """Reinicia os estados para começar uma nova rodada.
        """
        self.estados: List[Estado] = []
        self.estado: Estado = Estado()
        self.entregou = self.estado.entregou
        self.agarrou_objeto = False
        
    def _obter_resumo_execucao(self) -> List[Tuple[int, int]]:
        """Retorna uma resumo da execução com a quantidade
        """
        return self._resumo
    
    def _propagar_recompensa(self) -> None:
        """Realizar a propagação da recompensa para os Q values e reinicia
        as variáveis para uma próxima rodada.
        """
        recompensa = self.estado.obter_recompensa()
        for m in self.movimentos:
            self.tabela_q[self.estado.estado][m] = (recompensa, self.agarrou_objeto)
        for estado in reversed(self.estados):
            valor_q_atual = self.tabela_q[estado[0]][estado[1]][0]
            recompensa = valor_q_atual + self.taxa_aprendizado * (self.decaimento_gama * recompensa - valor_q_atual)
            self.tabela_q[estado[0]][estado[1]] = (recompensa, self.agarrou_objeto)
        self._reiniciar_estados()
        
    def _agarrar_objeto(
        self, 
        movimento
    ) -> None:
        """Agarra o objeto se estiver na posição correta.
        """
        
        if ((self.estado.estado == (2, 2) and movimento == 'direita') or 
            (self.estado.estado == (2, 4) and movimento == 'esquerda')) and not self.agarrou_objeto:
            self.agarrou_objeto = True
                
    def executar(
        self, 
        episodios: int=10, 
        verbose: bool = True
    ) -> None:
        """Executa rodadas de treinamento para o agente alcançar o objetivo.
        """
        episodio = 0
        passos = 0
        self.agarrou_objeto = False
        while episodio < episodios:
            if self.agarrou_objeto and self.estado.entregou_objeto:
                self._propagar_recompensa()
                resumo = {'episodio': episodio, 'passos': passos}
                print(resumo)
                print('-' * 120)
                self.resumo.append(resumo)
                passos = 0
                episodio += 1
            else:
                movimento = self._escolher_movimento()
                self.estados.append([(self.estado.estado), movimento])
                self._agarrar_objeto(movimento)
                msg = f"Posição atual em {self.estado.estado}, movimento para {movimento}, agarrou objeto: {self.agarrou_objeto},"
                self.estado = self._realizar_movimento(movimento)
                self.estado.entregou()
                
                if verbose:
                    print(f"{msg} próxima posição em {self.estado.estado}.")
                self.entregou = self.estado.entregou_objeto
                passos += 1