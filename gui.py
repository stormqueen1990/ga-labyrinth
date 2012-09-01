#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import constants
from PySide import QtCore, QtGui

# Monta a tela
class Tela(QtGui.QWidget):
	def __init__(self):
		super(Tela, self).__init__()
		self.setWindowTitle("Labirinto")

		# Seletor da população inicial
		self.txtPopInicial = QtGui.QSpinBox()
		self.txtPopInicial.setMinimum(54)
		self.txtPopInicial.setMaximum(200)

		# Seletor do tipo de seleção
		self.txtTipoSelecao = QtGui.QComboBox()
		self.txtTipoSelecao.addItem(constants.TipoCrossover.MAPA_ROTULO[constants.TipoCrossover.TORNEIO]
			, constants.TipoCrossover.TORNEIO)
		self.txtTipoSelecao.addItem(constants.TipoCrossover.MAPA_ROTULO[constants.TipoCrossover.APTIDAO]
			, constants.TipoCrossover.APTIDAO)

		# Seletor de taxa de mutação
		self.txtTaxaMutacao = QtGui.QDoubleSpinBox()
		self.txtTaxaMutacao.setRange(0.0, 100.0)

		# Seletor de taxa de crossover
		self.txtTaxaCrossover = QtGui.QDoubleSpinBox()
		self.txtTaxaCrossover.setRange(0.0, 100.0)

		# Tipo de crossover
		self.txtTipoCrossover = QtGui.QLineEdit()
		self.txtTipoCrossover.setInputMask("999")
		self.txtTipoCrossover.setAlignment(QtCore.Qt.AlignRight)
		self.txtTipoCrossover.setFixedWidth(30)
		self.txtTipoCrossover.setMaximumWidth(30)
		
		mainLayout = QtGui.QFormLayout()
		mainLayout.addRow("Popula\347\343o inicial:", self.txtPopInicial)
		mainLayout.addRow("Tipo de sele\347\343o:", self.txtTipoSelecao)
		mainLayout.addRow("Taxa de muta\347\343o:", self.txtTaxaMutacao)
		mainLayout.addRow("Taxa de crossover:", self.txtTaxaCrossover)
		mainLayout.addRow("Quantidade de pontos de crossover:", self.txtTipoCrossover)
		self.setLayout(mainLayout)

		self.resize(400, 400)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	tela = Tela()
	tela.show()
	
	app.exec_()
	sys.exit()
