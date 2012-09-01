#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import copy

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

class TiposParada:
	FITNESS = 1
	GERACOES = 2

class TipoCrossover:
	TORNEIO = 1
	APTIDAO = 2

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
		self.peso = 0

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

class Simulacao:
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

	# Pontua o caminho recebido de acordo com o mapa
	def __avaliaCaminho(self, individuo):
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
					if self.labirinto[posAtual.lin][posAtual.col] & \
						DirecoesBitwise.DIR_LESTE == 0:
						valCaminho = valCaminho + 10
					else:
						valCaminho = valCaminho + 30
			
					posAtual.col = posAtual.col + 1
				elif direcao == DirecoesVetor.DIR_NORTE:
					if self.labirinto[posAtual.lin][posAtual.col] & \
						DirecoesBitwise.DIR_NORTE == 0:
						valCaminho = valCaminho + 10
					else:
						valCaminho = valCaminho + 30

					posAtual.lin = posAtual.lin - 1
				elif direcao == DirecoesVetor.DIR_OESTE:
					if self.labirinto[posAtual.lin][posAtual.col] & \
						DirecoesBitwise.DIR_OESTE == 0:
						valCaminho = valCaminho + 10
					else:
						valCaminho = valCaminho + 30

					posAtual.col = posAtual.col - 1
				elif direcao == DirecoesVetor.DIR_SUL:
					if self.labirinto[posAtual.lin][posAtual.col] & \
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
	def __realizaCruzamento(self, ind1, ind2, numPontos):
		# Escolhe o menor comprimento
		if len(ind1) >= len(ind2):
			lenMenor = len(ind2)
		else:
			lenMenor = len(ind1)

		# O número de cortes não pode ser maior que
		# o comprimento do caminho
		if numPontos > lenMenor:
			numPontos = lenMenor

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

		# Atualiza os campos dos novos indivíduos
		ind1.custo = 0
		ind2.custo = 0
		ind1.tamanho = len(ind1.caminho) * 2
		ind2.tamanho = len(ind2.caminho) * 2

	# Gera a população, considerando a taxa de mutação
	def __geraPopulacaoInicial(self, tamanho, txMut):
		return [ Caminho(txMut) for i in range(tamanho) ]

	# Gera a próxima geração, a partir da anterior
	def __proximaGeracao(self, populacao, tipoCrossover, taxaCrossover,
		taxaMutacao, tipoSelecao):
		newPop = []
		popAtual = None

		# Verifica as aptidões
		if tipoSelecao == TipoSelecao.TORNEIO:
			random.seed()
			popAtual = populacao
		else:
			popPonderada = copy.deepcopy(populacao)
			roleta = []
			tot = 0
			valPeso = 0

			for ind in popPonderada:
				tot = tot + ind.custo
				valPeso = valPeso + (tot - indCusto)

			for ind in popPonderada:
				ind.peso = ((tot - ind.custo) * 100 / valPeso)

			popPonderada.sort(key=lambda peso: ind.peso, reverse = True)

			for ind in popPonderada:
				if ind.peso > 0:
					roleta.append(ind) for idx in range(ind.peso)

			popAtual = roleta

		# Gera nova população
		while len(newPop) < len(populacao):
			casal = copy.deepcopy(__sorteiaCasal(popAtual))
			txCross = random.randint()

			if txCross <= taxaCrossover:
				self.__realizaCruzamento(casal[0], casal[1])

			newPop.extend(casal)

		return newPop
	
	# Sorteia um casal para crossover
	def __sorteiaCasal(self, populacao):
		casal = []
		
		random.seed()
		while len(casal) < 2:
			pos1 = random.randint(0, len(populacao) - 1)
			pos2 = random.randint(0, len(populacao) - 1)

			if pos1 != pos2:
				if populacao[pos1].custo >= populacao[pos2].custo:
					casal.append(populacao[pos1])
				else:
					casal.append(populacao[pos2])

		return casal

	# Aplica elitismo nas gerações existentes
	def __elitismo(self, geracoes, tamPopulacao):
		novaPop = []
		todosIndividuos = []
		# Avalia os caminhos, caso haja algum sem avaliação
		for geracao in geracoes:
			for ind in geracao:
				if ind.custo == 0:
					__avaliaCaminho(ind)
			
			todosIndividuos.extend(geracao)
		
		# Ordena do menor para o maior custo
		todosIndividuos.sort(key=lambda custo: ind.custo)

		# Seleciona os n melhores
		for ind in todosIndividuos:
			if len(novaPop) == tamPopulacao:
				break

			novaPop.append(ind)

		return novaPop

	# Simulação total
	def simulacao(popInicial, tipoParada, valorParada, tipoCrossover,
		taxaCrossover, taxaMutacao, tipoSelecao):
		populacao = self.__geraPopulacaoInicial(popInicial, taxaMutacao)
		geracoes = [populacao]

		if tipoParada == TiposParada.FITNESS:
			paradaFitness = False
			
			while not paradaFitness:
				for ind in populacao:
					self.__avaliaCaminho(pop)

					if pop.custo <= valorParada:
						paradaFitness = True
						break

				geracoes.append(__proximaGeracao(populacao, tipoCrossover,
					taxaCrossover, taxaMutacao, tipoSelecao)
				geracoes = [ __elitismo(geracoes, len(populacao)) ]
		else:
			ctGeracao = 1

			while ctGeracao < valorParada:
				self.__avaliaCaminho(pop)
				
				geracoes.append(__proximaGeracao(populacao, tipoCrossover,
					taxaCrossover, taxaMutacao, tipoSelecao)
				geracoes = [ __elitismo(geracoes, len(populacao)) ]

				ctGeracao = ctGeracao + 1
	
if __name__ == "__main__":
	s = Simulador()
