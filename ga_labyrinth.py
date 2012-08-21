#!/usr/bin/env python
import random

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

class Caminho:
	def __init__(self):
		random.seed()
		self.tamanho = random.randint(MIN_TAM_CAMINHO, MAX_TAM_CAMINHO)
		self.custo = 0
		self.caminho = self.__geraCaminho(self.tamanho)

		print(self.caminho)

	def __geraCaminho(self, tamanho):
		caminho = []
		x = 0

		while x < tamanho:
			item = random.randint(0,3)
			caminho.append(DIRS[item])
			x = x + 1

		return caminho

	def __unicode__(self):
		return u"Caminho[" + `self.tamanho` + ", " + `self.custo` + ", " + `self.caminho` + "]" 
		
# Pontua o caminho recebido de acordo com o mapa
def avaliaCaminho(individuo):
	valCaminho = 0
	posAtual = [9,0]
	ultPos = []

	try:
		for str in individuo.caminho:
			ultPos = posAtual
			if str == DIR_LESTE_STR:
				if labirinto[posAtual[0]][posAtual[1]] & DIR_LESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30
	
				posAtual[1] = posAtual[1] + 1
			elif str == DIR_NORTE_STR:
				if labirinto[posAtual[0]][posAtual[1]] & DIR_NORTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual[0] = posAtual[0] - 1
			elif str == DIR_OESTE_STR:
				if labirinto[posAtual[0]][posAtual[1]] & DIR_OESTE == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual[1] = posAtual[1] - 1
			elif str == DIR_SUL_STR:
				if labirinto[posAtual[0]][posAtual[1]] & DIR_SUL == 0:
					valCaminho = valCaminho + 10
				else:
					valCaminho = valCaminho + 30

				posAtual[0] = posAtual[0] + 1

		if len(ultPos) == 2:
			if ultPos != [0,9]:
				valCaminho = valCaminho + 60
	except IndexError:
		valCaminho = 1000

	return valCaminho

if __name__ == "__main__":
	caminho = Caminho()
	print(avaliaCaminho(caminho))
