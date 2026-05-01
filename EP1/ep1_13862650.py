import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


LINHAS_n = 5
INTERVALO_T = 50
PARAMETRO_exp = 3
TEMPO_ATENDIMENTO = 40
LOOP = 500
ERRO = -1

class Guiche:
    def __init__(self, id, tempo):
        self.id = id
        self.tempoOcupado = tempo

    def __repr__(self):
        return f"Guiche(id={self.id}, tempo={self.tempoOcupado})"


class Requisicao:
    def __init__(self, id, tempo):
        self.id = id
        self.tempoDeAtendimento = tempo

    def __repr__(self):
        return f"Requisicao(id={self.id}, tempo={self.tempoDeAtendimento})"    


def fluxoDeRequisicoes(tempoAtual):
    z = int(1 + random.expovariate(1/PARAMETRO_exp))
    proximoTempo = tempoAtual + z 
    
    return 1


def tempoDeAtendimento():
    z = int(1 + random.expovariate(1/TEMPO_ATENDIMENTO))
    return 20


def verificaDisponibilidadeDasLinhas(guiche):
    for i in range(len(guiche)):
        if guiche[i].tempoOcupado == 0:
            return i

    return ERRO


def atendimento(guiche, fila, atendidos, rejeitados):
    while fila:
        livre = verificaDisponibilidadeDasLinhas(guiche)
        primeiro = fila.popleft()
        
        if livre is not ERRO:
            guiche[livre].tempoOcupado = primeiro.tempoDeAtendimento

            atendidos.append(primeiro)
        else:
            #esse é o momento em que deve ser adicionado o codigo referente ao cliente esperar ou ser rejeitado
            rejeitados.append(primeiro)


def testaGuiche(guiche):
    for i in range(len(guiche)):
        if guiche[i].tempoOcupado > 0:
            guiche[i].tempoOcupado -= 1        
        

def calculoDeAceitacao(atendidos):
    atd = len(atendidos)

    return atd


def calculoDeRejeicao(rejeitados):
    rej = len(rejeitados)

    return rej


def calculoDeProporcao(atendidos, rejeitados):
    proporcao = rejeitados/(atendidos + rejeitados)

    return proporcao

def calculoDeMedias(lista):
    media = np.mean(lista)

    return media


def numInteracoes(i):
    iteracoes = LOOP + LOOP*i
    return iteracoes


def paradaDoPrograma(fila, n):
    s = np.std(fila, ddof=1)  # desvio padrão amostral
    erro_padrao = s / np.sqrt(n)

    if(2 * 1.96 * erro_padrao < 0.002):
        return True
    
    return False


def decisaoDeEntrarNaFila():
    pass


def main():
    while(True):
        i = 0
        k = numInteracoes(i)
        i += 1

        for p in range(k):
            guiche = [Guiche(i+1, 0) for i in range(LINHAS_n)]
            
            fila = deque()

            atendidos = []
            rejeitados = []
            proporcaoRejeitados = []

            totalAceitos = []
            totalRejeitados = []
            
            proxRequisicao = 0
            idRequisicao = 0

            for j in range(INTERVALO_T):

                if proxRequisicao == 0:
                    proxRequisicao = fluxoDeRequisicoes(proxRequisicao)
            
                    if j + proxRequisicao > INTERVALO_T:
                        proxRequisicao -= 1
                        continue
                    
                    tempo = tempoDeAtendimento()

                    req = Requisicao(idRequisicao, tempo)
                    fila.append(req)
                    
                    idRequisicao += 1
                else:
                    proxRequisicao -= 1
                        
                atendimento(guiche, fila, atendidos, rejeitados)
                testaGuiche(guiche)

            totalAceitos.append(calculoDeAceitacao(atendidos))
            totalRejeitados.append(calculoDeRejeicao(rejeitados))
            proporcaoRejeitados.append(calculoDeProporcao(len(atendidos), len(rejeitados)))

        mediaAceitos = calculoDeMedias(totalAceitos) 
        mediaRejeitados = calculoDeMedias(totalRejeitados)
        mediaProporcoes = calculoDeMedias(proporcaoRejeitados)

        if paradaDoPrograma(proporcaoRejeitados):
            break

        
if __name__ == '__main__':
    main()
