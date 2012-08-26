#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# Mapa do labirinto
# Representação por bits: 0001 é parede a sul,
# 0010 é parede a oeste, 0100 é parede a norte
# e 1000 é parede a leste
#   N
# O + L
#   S
labirinto = [
				[ 6,  5,  5,  5, 12,  6,  5,  5, 12,  6],
				[10,  7,  5,  5,  9, 10,  6, 12,  3,  9],
				[ 2,  5,  5,  5,  5,  8, 11,  2,  5, 12],
				[ 3,  5,  5, 12,  7,  1,  5,  9, 14, 10],
				[ 6, 13,  6,  8,  6,  5,  5,  5,  9,  3],
				[ 3,  5,  8,  2,  1,  5,  5,  5,  5, 12],
				[ 6,  5,  9, 10,  7,  4, 12,  6,  5,  9],
				[ 2,  4,  5,  1,  4,  8,  2,  3,  5, 12],
				[10, 10,  7, 13, 10, 10,  3,  5,  5,  8],
				[ 9,  3,  5,  5,  9,  3,  5,  5,  5,  9],
			]

# Constantes usadas
class DirecoesBitwise:
	DIR_LESTE = 8
	DIR_NORTE = 4
	DIR_OESTE = 2
	DIR_SUL   = 1

class DirecoesVetor:
	DIR_LESTE = [0, 0]
	DIR_NORTE = [0, 1]
	DIR_OESTE = [1, 0]
	DIR_SUL   = [1, 1]

class TamanhoCaminho:
	MINIMO = 54
	MAXIMO = 200

# Abstração do caminho
class Caminho:
	INV_MAP = {0 : 1, 1 : 0}

	# Inicializa cada caminho
	def __init__(self, txMutacao):
		random.seed()
		self.tamanho = random.randint(TamanhoCaminho.MINIMO, TamanhoCaminho.MAXIMO)

		if self.tamanho % 2 == 1:
			self.tamanho = self.tamanho + 1

		self.custo = 0
		self.caminho = self.__geraCaminho(self.tamanho, txMutacao)
		self.punicao = False

	# Gera um caminho aleatoriamente
	def __geraCaminho(self, tamanho, txMutacao):
		caminho = [ random.randint(0,1) for x in range(tamanho) ]

		if txMutacao > 0:
			for pos in range(tamanho):
				chance = random.randint(1, 100)

				if chance <= txMutacao:
					item = caminho[pos]
					caminho[pos] = self.INV_MAP[item]

		newCaminho = []
		for i in range(0, tamanho - 1, 2):
			newCaminho.append(caminho[i:i+2])

		return newCaminho

	# Printa o objeto
	def __str__(self):
		return u"Caminho[" + `self.tamanho` + ", " + `self.custo` + ", " + `self.caminho` + "]" 

# Abstração de ponto
class Ponto:
	def __init__(self, lin, col):
		self.lin = lin
		self.col = col
		
# Pontua o caminho recebido de acordo com o mapa
def avaliaCaminho(individuo):
	valCaminho = 0
	posAtual = Ponto(0,9)
	ultPos = None

	# Segue as coordenadas do caminho
	for direcao in individuo.caminho:
		ultPos = posAtual

		# Escapou do labirinto. +100 pra cada casa andada
		if individuo.punicao:
			valCaminho = valCaminho + 100
		else:
			# Verifica cada direção se tem parede ou não e soma um valor
			if direcao == DirecoesVetor.DIR_LESTE:
				if labirinto[posAtual.lin][posAtual.col] & \
					DirecoesBitwise.DIR_LESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30
		
				posAtual.col = posAtual.col + 1
			elif direcao == DirecoesVetor.DIR_NORTE:
				if labirinto[posAtual.lin][posAtual.col] & \
					DirecoesBitwise.DIR_NORTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual.lin = posAtual.lin - 1
			elif direcao == DirecoesVetor.DIR_OESTE:
				if labirinto[posAtual.lin][posAtual.col] & \
					DirecoesBitwise.DIR_OESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual.col = posAtual.col - 1
			elif direcao == DirecoesVetor.DIR_SUL:
				if labirinto[posAtual.lin][posAtual.col] & \
					DirecoesBitwise.DIR_SUL == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual.lin = posAtual.lin + 1

			# Fugiu do labirinto!!
			if posAtual.lin in [-1, 10] \
				or posAtual.col in [-1, 10]:
				individuo.punicao = True
		
	# Não atingiu a saída do labirinto
	if ultPos != None \
		and ultPos.lin != 0 \
		and ultPos.col != 9:
		valCaminho = valCaminho + 60

	# Atribui o custo ao indivíduo
	individuo.custo = valCaminho

# Realiza o crossover de dois indivíduos
def realizaCruzamento(ind1, ind2, numPontos):
	# Escolhe o menor comprimento
	if len(ind1) >= len(ind2):
		lenMenor = len(ind2)
	else:
		lenMenor = len(ind1)

	numCortes = 0
	posCorte = lenMenor / numPontos

	# Percorre o caminho, cortando as partes e trocando-as
	x = 0
	while currPos < lenMenor:
		y = x + posCorte

		if numCortes % 2 == 1:
			aux = ind1.caminho[x:y]
			ind1.caminho[x:y] = ind2.caminho[x:y]
			ind2.caminho[x:y] = aux

		numCortes = numCortes + 1
		x = y

# Gera a população, considerando a taxa de mutação
def geraPopulacaoInicial(tamanho, txMut):
	return [ Caminho(txMut) for i in range(tamanho) ]
	
if __name__ == "__main__":
	populacao = geraPopulacaoInicial(50, 4)
	for individuo in populacao:
		avaliaCaminho(individuo)
		print(individuo.custo)
