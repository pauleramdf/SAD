import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import csv
import math
import random
#import sqlalchemy
from decimal import Decimal
import copy
#import pandas as pd

class SideMenu(Frame):
    def __init__(self, controller, parent):
        self.parent = parent
        self.controller = controller
        self.container = Frame(parent)
        self.container.pack(side=RIGHT)
        self.qualidadeBefore = StringVar()
        self.qualidadeAfter = StringVar()
        self.diferenca = StringVar()
        self.taxaOcup = StringVar()
        self.makewidgets()

    def makewidgets(self): 
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.qualidadeBefore.set("Qualidade Inicial = 0")
        self.qualidadeAfter.set("Qualidade Otimizada = 0")
        self.diferenca.set("Melhora obtida foi de = 0")
        self.taxaOcup.set("A taxa de ocupação foi = 0")

        self.labelqBefore = tk.Label(self.container, text= "teste",textvariable = self.qualidadeBefore)
        self.labelqAfter = tk.Label(self.container, textvariable = self.qualidadeAfter)
        self.labelDiferenca = tk.Label(self.container, textvariable = self.diferenca)
        self.labelTaxaOcup = tk.Label(self.container, textvariable = self.taxaOcup)

        self.labelH = tk.Label(self.container,text= "Lista de horarios")
        self.labelT = tk.Label(self.container,text= "Lista de turmas")
        self.listaTurmas  = ttk.Combobox(self.container, justify=CENTER, values = ["Horarios da turma"])
        self.listaTurmas2  = ttk.Combobox(self.container,justify=CENTER, values=["Salas Disponiveis"])
        self.trocar = Button(self.container, text="Trocar",command=self.trocarTurmas)
        self.carregar1 = Button(self.container, text="Carregar Solucao1",command=self.carregarSolucao1)
        self.salvar1 = Button(self.container, text="Salvar Solucao1",command=self.salvarSolucao1)

        self.carregar2 = Button(self.container, text="Carregar Solucao2",command=self.carregarSolucao2)
        self.salvar2 = Button(self.container, text="Salvar Solucao2",command=self.salvarSolucao2)

    def setup_layout(self):
        self.listaTurmas.current(0)
        self.listaTurmas2.current(0)
        self.labelqBefore.pack()
        self.labelqAfter.pack()
        self.labelDiferenca.pack()
        self.labelTaxaOcup.pack()
        self.labelH.pack()
        self.listaTurmas.pack()
        self.labelT.pack()
        self.listaTurmas2.pack()
        self.trocar.pack()
        self.carregar1.pack()
        self.salvar1.pack()
        self.carregar2.pack()
        self.salvar2.pack()

    def trocarTurmas(self):
        horario = self.listaTurmas.get()
        sala_futura = self.listaTurmas2.get()

        linha = self.controller.getLinha()
        sala_atual = linha[0]
        dia, hora = horario.split(" ")
        hora = int(hora)

        #print("trocar a turma",linha[4] ,"no horario", self.listaTurmas.get(),"com", self.listaTurmas2.get())
        self.controller.trocaTurmas((sala_atual, sala_futura), dia, hora)

    def setQualidadeBefore(self, qualidade):
        self.qualidadeBefore.set("Qualidade Inicial = {q: .5f}".format(q = qualidade))

    def setQualidadeAfter(self, qualidade):
        self.qualidadeAfter.set("Qualidade Otimizada = {q: .5f}".format(q = qualidade))

    def setDiferenca(self, a, b):
        self.diferenca.set("Melhora obtida foi de = {q: .3f}%".format(q = (b - a)/b *100))
    
    def setTaxaOCup(self, taxa):
        self.taxaOcup.set("A taxa de ocupação foi de = {q: .3f}".format(q = taxa))
    
    def setHorarioTurma(self, valores):
        id_turma = valores[4]
        lista = []

        horariosPossiveis = self.controller.getHorarioTurma(id_turma)
        for h in horariosPossiveis:
            lista.append(str(h[0]) + " " + str(h[1]))

        self.listaTurmas['values'] = lista

    def setListaTurmas(self, valores):
        id_turma = valores[4]
        lista = []

        salasPossiveis = self.controller.getSalasPossiveis(id_turma)
        for sala in salasPossiveis:
            lista.append(str(sala[0]))
        self.listaTurmas2['values'] = lista

        #[('101', {'cad': 100, 'acess': 1, 'quali': 1}), ('201', {'cad': 100, 'acess': 1, 'quali': 2}), ('301', {'cad': 100, 'acess': 1, 'quali': 2})]
    def salvarSolucao1(self):
        self.controller.salvarSolucao1()

    def salvarSolucao2(self):
        self.controller.salvarSolucao2()

    def carregarSolucao1(self):
        self.controller.carregarSolucao1()
    
    def carregarSolucao2(self):
        self.controller.carregarSolucao2()
        
