#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import constants
import simulation
from PySide import QtCore, QtGui

# Interface do usuário
class Tela(QtGui.QWidget):
	def __init__(self):
		super(Tela, self).__init__()
		self.setWindowTitle(self.trUtf8("Labirinto"))

		# Seletor da população inicial
		self.txtPopInicial = QtGui.QSpinBox()
		self.txtPopInicial.setMinimum(20)
		self.txtPopInicial.setMaximum(10000)

		# Seletor do tipo de seleção
		self.txtTipoSelecao = QtGui.QComboBox()
		self.txtTipoSelecao.addItem(self.trUtf8(constants.TipoSelecao.MAPA_ROTULO[constants.TipoSelecao.TORNEIO])
			, constants.TipoSelecao.TORNEIO)
		self.txtTipoSelecao.addItem(self.trUtf8(constants.TipoSelecao.MAPA_ROTULO[constants.TipoSelecao.APTIDAO])
			, constants.TipoSelecao.APTIDAO)

		# Seletor do tipo de parada da simulação
		self.txtTipoParada = QtGui.QComboBox()
		self.txtTipoParada.addItem(self.trUtf8(constants.TiposParada.MAPA_ROTULO[constants.TiposParada.FITNESS])
			, constants.TiposParada.FITNESS)
		self.txtTipoParada.addItem(self.trUtf8(constants.TiposParada.MAPA_ROTULO[constants.TiposParada.GERACOES])
			, constants.TiposParada.GERACOES)
		
		# Número de gerações para parada
		self.txtValorParada = QtGui.QSpinBox()
		self.txtValorParada.setMinimum(1)
		self.txtValorParada.setMaximum(10000)

		# Seletor de taxa de mutação
		self.txtTaxaMutacao = QtGui.QSpinBox()
		self.txtTaxaMutacao.setRange(0, 100)

		# Seletor de taxa de crossover
		self.txtTaxaCrossover = QtGui.QSpinBox()
		self.txtTaxaCrossover.setRange(0, 100)

		# Tipo de crossover
		self.txtTipoCrossover = QtGui.QSpinBox()
		self.txtTipoCrossover.setRange(1, 200)

		# Tamanho mínimo e máximo do caminho
		self.txtMinTamCaminho = QtGui.QSpinBox()
		self.txtMinTamCaminho.setRange(27, 100)
		
		self.txtMaxTamCaminho = QtGui.QSpinBox()
		self.txtMaxTamCaminho.setRange(27, 100)

		# Campos lado a lado
		tamCaminhoLayout = QtGui.QHBoxLayout()
		tamCaminhoLayout.addWidget(self.txtMinTamCaminho)
		tamCaminhoLayout.addWidget(QtGui.QLabel(self.trUtf8(" até ")))
		tamCaminhoLayout.addWidget(self.txtMaxTamCaminho)
		tamCaminhoLayout.addWidget(QtGui.QLabel(self.trUtf8("direções")))

		# Botões para iniciar a simulação e sair do programa
		self.btnIniciarSimulacao = QtGui.QPushButton(self.trUtf8("Iniciar"), self)
		self.btnIniciarSimulacao.clicked.connect(self.realizaSimulacao)

		self.btnSairJanela = QtGui.QPushButton(self.trUtf8("Sair"), self)
		self.btnSairJanela.clicked.connect(self.sair)

		# Listagem dos resultados
		self.listagemResultados = QtGui.QTreeView()
		self.modeloListagem = QtGui.QStandardItemModel(0, 3, self)
	
		# Cabeçalhos da listagem
		self.modeloListagem.setHeaderData(0, QtCore.Qt.Horizontal, self.trUtf8("Tamanho"));
		self.modeloListagem.setHeaderData(1, QtCore.Qt.Horizontal, self.trUtf8("Custo"));
		self.modeloListagem.setHeaderData(2, QtCore.Qt.Horizontal, self.trUtf8("Direções"));

		self.listagemResultados.setModel(self.modeloListagem)
	
		# Formulário de seleção dos parâmetros
		paramFormLayout = QtGui.QFormLayout()
		paramFormLayout.addRow(self.trUtf8("População inicial:"), self.txtPopInicial)
		paramFormLayout.addRow(self.trUtf8("Tipo de parada:"), self.txtTipoParada)
		paramFormLayout.addRow(self.trUtf8("Valor para parada"), self.txtValorParada)
		paramFormLayout.addRow(self.trUtf8("Tipo de seleção:"), self.txtTipoSelecao)
		paramFormLayout.addRow(self.trUtf8("Taxa de mutação:"), self.txtTaxaMutacao)
		paramFormLayout.addRow(self.trUtf8("Taxa de crossover:"), self.txtTaxaCrossover)
		paramFormLayout.addRow(self.trUtf8("Qtd. pontos de crossover:"), self.txtTipoCrossover)
		paramFormLayout.addRow(self.trUtf8("Tamanho do caminho:"), tamCaminhoLayout)

		paramForm = QtGui.QWidget()
		paramForm.setLayout(paramFormLayout)

		# Botões de ação
		barraBotoesLayout = QtGui.QHBoxLayout()
		barraBotoesLayout.setAlignment(QtCore.Qt.AlignCenter)
		barraBotoesLayout.addWidget(self.btnIniciarSimulacao)
		barraBotoesLayout.addWidget(self.btnSairJanela)

		barraBotoes = QtGui.QWidget()
		barraBotoes.setLayout(barraBotoesLayout)

		# Tabela dos resultados
		containerTabela = QtGui.QGroupBox(self.trUtf8("Resultados"))
		layoutContTabela = QtGui.QHBoxLayout()
		layoutContTabela.addWidget(self.listagemResultados)
		containerTabela.setLayout(layoutContTabela)

		# Montagem do layout
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(paramForm)
		mainLayout.addWidget(barraBotoes)
		mainLayout.addWidget(containerTabela)
		
		mainBox = QtGui.QWidget()
		mainBox.setLayout(mainLayout)

		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(mainBox)

		self.setLayout(hlayout)
	
	# Adiciona um resultado à listagem
	def __novoResultado(self, caminho):
		self.modeloListagem.insertRow(0)
		self.modeloListagem.setData(self.modeloListagem.index(0, 0),
			caminho.tamanho/2)
		self.modeloListagem.setData(self.modeloListagem.index(0, 1),
			caminho.custo)
		self.modeloListagem.setData(self.modeloListagem.index(0, 2),
			caminho.caminhoStr())
	
	# Realiza a simulação
	def realizaSimulacao(self):
		simulacao = simulation.Simulacao()

		popInicial = self.txtPopInicial.value()
		tipoSelecao = self.txtTipoSelecao.itemData(self.txtTipoSelecao.currentIndex())
		tipoParada = self.txtTipoParada.itemData(self.txtTipoParada.currentIndex())
		valorParada = self.txtValorParada.value()
		taxaMutacao = self.txtTaxaMutacao.value()
		taxaCrossover = self.txtTaxaCrossover.value()
		tipoCrossover = self.txtTipoCrossover.value()
		minTamanho = self.txtMinTamCaminho.value() * 2
		maxTamanho = self.txtMaxTamCaminho.value() * 2

		resultados = simulacao.simulacao(popInicial, tipoParada, valorParada,
			tipoCrossover, taxaCrossover, taxaMutacao, tipoSelecao, minTamanho,
			maxTamanho)
		
		if self.modeloListagem.rowCount() > 0:
			self.modeloListagem.removeRows(0, self.modeloListagem.rowCount())

		for ind in resultados:
			self.__novoResultado(ind)

	# Sai do programa
	def sair(self):
		sys.exit()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	tela = Tela()
	tela.show()

	app.exec_()
	sys.exit()
