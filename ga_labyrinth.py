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
DIR_LESTE_STR = "00"
DIR_NORTE_STR = "01"
DIR_OESTE_STR = "10"
DIR_SUL_STR   = "11"

DIRS = [DIR_LESTE_STR
       ,DIR_NORTE_STR
	   ,DIR_OESTE_STR
	   ,DIR_SUL_STR]

DIR_LESTE = 8
DIR_NORTE = 4
DIR_OESTE = 2
DIR_SUL   = 1

MIN_TAM_CAMINHO = 27
MAX_TAM_CAMINHO = 100

mapaMutacao = { "00" : ["01", "10"]
			  , "01" : ["11", "00"]
			  , "10" : ["11", "00"]
			  , "11" : ["10", "01"] }

# Abstração do caminho
class Caminho:
	# Inicializa cada caminho
	def __init__(self):
		random.seed()
		self.tamanho = random.randint(MIN_TAM_CAMINHO, MAX_TAM_CAMINHO)
		self.custo = 0
		self.caminho = self.__geraCaminho(self.tamanho)
		self.punicao = False

	# Gera um caminho aleatoriamente
	def __geraCaminho(self, tamanho):
		caminho = [ DIRS[random.randint(0,3)] for x in range(tamanho) ]

		return caminho

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
	for str in individuo.caminho:
		ultPos = posAtual

		# Escapou do labirinto. +100 pra cada casa andada
		if individuo.punicao:
			valCaminho = valCaminho + 100
		else:
			# Verifica cada direção se tem parede ou não e soma um valor
			if str == DIR_LESTE_STR:
				if labirinto[posAtual.lin][posAtual.col] & DIR_LESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30
		
				posAtual.col = posAtual.col + 1
			elif str == DIR_NORTE_STR:
				if labirinto[posAtual.lin][posAtual.col] & DIR_NORTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual.lin = posAtual.lin - 1
			elif str == DIR_OESTE_STR:
				if labirinto[posAtual.lin][posAtual.col] & DIR_OESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual.col = posAtual.col - 1
			elif str == DIR_SUL_STR:
				if labirinto[posAtual.lin][posAtual.col] & DIR_SUL == 0:
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
	lenInd1 = len(ind1)
	lenInd2 = len(ind2)
	lenMenor = None
	posCorte = None

	# Escolhe o menor comprimento
	if lenInd1 >= lenInd2:
		lenMenor = lenInd2
	else:
		lenMenor = lenInd1

	numCortes = 0

	# Percorre o caminho, cortando as partes e trocando-as
	while currPos < lenMenor:
		x = currPos
		y = currPos + posCorte

		if numCortes % 2 == 1:
			aux = ind1.caminho[x:y]
			ind1.caminho[x:y] = ind2.caminho[x:y]
			ind2.caminho[x:y] = aux

		numCortes = numCortes + 1

# Gera a população, considerando a taxa de mutação
def geraPopulacao(tamanho, txMut):
	pop = [ Caminho() for i in range(tamanho) ]
	
	for ind in pop:
		print(ind.tamanho)

if __name__ == "__main__":
	print(Caminho())
