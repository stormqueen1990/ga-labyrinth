#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import *

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
	
	@staticmethod
	def converteTexto(parte):
		if parte == DirecoesVetor.DIR_LESTE:
			return "L"
		elif parte == DirecoesVetor.DIR_NORTE:
			return "N"
		elif parte == DirecoesVetor.DIR_OESTE:
			return "O"
		elif parte == DirecoesVetor.DIR_SUL:
			return "S"

class TamanhoCaminho:
	MINIMO = 54
	MAXIMO = 200

class TiposParada:
	FITNESS = 1
	GERACOES = 2
	MAPA_ROTULO = { FITNESS : "Aptidão"
			      , GERACOES : "Número de gerações" }

class TipoSelecao:
	TORNEIO = 1
	APTIDAO = 2
	MAPA_ROTULO = { TORNEIO : "Torneio"
				  , APTIDAO : "Aptidão" }
