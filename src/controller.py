import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from Views.topMenu import TopMenu
from Views.sideMenu import SideMenu
from Views.tabela import Tabela
from Views.busca import Busca
from Model.simulatedAnnealing import Model

class Controller:
    def __init__(self, parent):
        #inicializa os frames
        self.parent = parent
        self.topMenu = TopMenu(self, parent)
        self.tabela = Tabela(self, parent)
        self.sideMenu = SideMenu(self, parent)
        self.model = Model(self, parent)

    def getLinha(self):
        #pega a informação da tabela que foi clicada 
        info = self.tabela.getLinha()
        return info

    def trocaTurmas(self, salas, dia, horario):
        #recebe do SideBar as salas selecioonadas para troca e os horarios.
        #Então chama a função trocaTurma no Model que efetivamente faz a troca.
        #Por fim os valores das qualidades são atualizados na GUI 
        try:
            self.model.trocarTurma(salas, dia, horario)
            self.tabela.updateTabela(self.model.exibeSolucao((self.model.otimizacao)))
            self.model.updateQualidade()
            self.sideMenu.setQualidadeBefore(self.model.qBefore)
            self.sideMenu.setQualidadeAfter(self.model.qAfter)
            self.sideMenu.setDiferenca(self.model.qBefore, self.model.qAfter)
            self.sideMenu.setTaxaOCup(self.model.taxaOcup)
        except:
           messagebox.showinfo(title="ERRO", message="Sala ou Horario invalido")
        
    def otimizacao_btn_pressed( self, pesos, temp, fator, maxIterations, pathTurmas, pathSalas):
        #Essa função recebe os parametros passados pelo usuario para começar o SimulatedAnnealing.
        #A otimização é realizada no model e então os valores das qualidades são atualizados na GUI
        #try:
        (qBefore, qAfter) = self.model.solucao(pesos, temp, fator, maxIterations, pathTurmas, pathSalas)
        self.sideMenu.setQualidadeBefore(qBefore)
        self.sideMenu.setQualidadeAfter(qAfter)
        self.sideMenu.setDiferenca(qBefore, qAfter)
        self.sideMenu.setTaxaOCup(self.model.taxaOcup)
        self.tabela.setTabela(self.model.exibeSolucao(self.model.otimizacao))
        #except:
         #   messagebox.showinfo(title="ERRO", message="Parametros invalidos")
    
    #recebe a lista de turmas compativeis com a turma clicada e atualiza a lista no SideMenu
    def setListaTurmas(self, valores):
        self.sideMenu.setListaTurmas(valores)
   
    #recebe uma lista de horarios e atualiza a lista no SideMenu de acordo com a linha clicada na tabela
    def setHorarioTurma(self, valores):
        self.sideMenu.setHorarioTurma(valores)

    #Rebece o id da turma na linha que foi clidada e então faz a busca das salas compativeis com a respectiva turma
    def getSalasPossiveis(self, id_turma):
        salasPossiveis = self.model.listaSalasPossiveis(id_turma)
        return salasPossiveis

    #Rebece o id da turma na linha que foi clidada e então faz a busca dos horarios da respectiva turma
    def getHorarioTurma(self, id_turma):
        horariosPossiveis = self.model.getHorarioTurma(id_turma)
        return horariosPossiveis
    
    #Cria a janela responsavel por buscar as informações sobre as turmas
    def buscarTurmas(self):
        busca = Busca(self, self.model.turmas, self.model.salas, 1)
        busca.inicia()

    #Cria a janela responsavel por buscar as informações sobre as salas
    def buscarSalas(self):
        busca = Busca(self, self.model.turmas, self.model.salas, 0)
        busca.inicia()
    
    #Salva uma tabela no banco de dados com os dados da solução 
    def salvarSolucao(self):
        try:
            self.model.salvarSolucao()
            messagebox.showinfo(title="SUCESSO", message="Solução foi salva com sucesso")
        except:
            messagebox.showinfo(title="ERRO", message="Solução não foi salva")

    #Carrega uma tabela no banco de dados que representa uma solução valida
    #Apos isso os dados das qualidades são atualizados.
    def carregarSolucao(self):
        try:
            self.tabela.updateTabela(self.model.carregarSolucao())
            self.model.updateQualidade()
            self.sideMenu.setQualidadeBefore(self.model.qBefore)
            self.sideMenu.setQualidadeAfter(self.model.qAfter)
            self.sideMenu.setDiferenca(self.model.qBefore, self.model.qAfter)
            self.sideMenu.setTaxaOCup(self.model.taxaOcup)
        except:
            messagebox.showinfo(title="ERRO", message="Solução não foi carregada")

    #reverte todas as alterações feitas na solução encontrada pelo SimulatedAnnealing 
    # ou na solução carregada do banco de dados. Apos isso, os dados das qualidades 
    #são atualizados.
    def reverterAlteracoes(self):
        self.model.reverterAlteracoes()
        self.tabela.updateTabela(self.model.exibeSolucao(self.model.otimizacao))
        self.model.updateQualidade()
        self.sideMenu.setQualidadeBefore(self.model.qBefore)
        self.sideMenu.setQualidadeAfter(self.model.qAfter)
        self.sideMenu.setDiferenca(self.model.qBefore, self.model.qAfter)
        self.sideMenu.setTaxaOCup(self.model.taxaOcup)

        
if __name__ == "__main__":
    root = Tk()
    WIDTH = 1100
    HEIGHT = 600
    root.title("Alocação de turmas")
    root.geometry("%sx%s" % (WIDTH, HEIGHT))

    window = Controller(root)

    root.mainloop()
