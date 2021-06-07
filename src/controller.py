import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from Views.topMenu import TopMenu
from Views.sideMenu import SideMenu
from Views.tabela import Tabela
from Model.simulatedAnnealing import Model

class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.topMenu = TopMenu(self, parent)
        self.tabela = Tabela(self, parent)
        self.sideMenu = SideMenu(self, parent)
        self.model = Model(self, parent)

    def getLinha(self):
        info = self.tabela.getLinha()
        return info

    def trocaTurmas(self, salas, dia, horario):
        self.model.trocarTurma(salas, dia, horario)
        self.tabela.updateTabela(self.model.exibeSolucao((self.model.otimizacao)))

    def otimizacao_btn_pressed( self, peso, temp, fator, maxIterations, pathTurmas, pathSalas):
        try:
            (qBefore, qAfter) = self.model.solucao(peso, temp, fator, maxIterations, pathTurmas, pathSalas)
            self.sideMenu.setQualidadeBefore(qBefore)
            self.sideMenu.setQualidadeAfter(qAfter)
            self.sideMenu.setDiferenca(qBefore, qAfter)
            self.sideMenu.setTaxaOCup(self.model.taxaOcup)
            self.tabela.setTabela(self.model.exibeSolucao(self.model.otimizacao))
        except:
            messagebox.showinfo(title="ERRO", message="Parametros invalidos")
    
    def setListaTurmas(self, valores):
        self.sideMenu.setListaTurmas(valores)

    def setHorarioTurma(self, valores):
        self.sideMenu.setHorarioTurma(valores)

    def getSalasPossiveis(self, id_turma):
        salasPossiveis = self.model.listaSalasPossiveis(id_turma)
        return salasPossiveis

    def getHorarioTurma(self, id_turma):
        horariosPossiveis = self.model.getHorarioTurma(id_turma)
        return horariosPossiveis
    
    def salvarSolucao(self):
        self.model.salvarSolucao()



        
if __name__ == "__main__":
    root = Tk()
    WIDTH = 1000
    HEIGHT = 600
    root.geometry("%sx%s" % (WIDTH, HEIGHT))

    window = Controller(root)

    root.mainloop()