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
        self.makewidgets()

    def makewidgets(self): 
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.qualidadeBefore.set("Qualidade Inicial = 0")
        self.qualidadeAfter.set("Qualidade Otimizada = 0")
        self.diferenca.set("Melhora obtida foi de = 0")

        self.labelqBefore = tk.Label(self.container, text= "teste",textvariable = self.qualidadeBefore)
        self.labelqAfter = tk.Label(self.container, textvariable = self.qualidadeAfter)
        self.labelDiferenca = tk.Label(self.container, textvariable = self.diferenca)
        self.label3 = tk.Label(self.container,text= "Lista de turmas")
        self.listaTurmas  = ttk.Combobox(self.container, justify=CENTER, values = ["Horarios da turma"])
        self.listaTurmas2  = ttk.Combobox(self.container,justify=CENTER, values=["Salas Disponiveis"])
        self.trocar = Button(self.container, text="Trocar",command=self.trocarTurmas)

    def setup_layout(self):
        self.listaTurmas.current(0)
        self.listaTurmas2.current(0)
        self.labelqBefore.pack()
        self.labelqAfter.pack()
        self.labelDiferenca.pack()
        self.label3.pack()
        self.listaTurmas.pack()
        self.listaTurmas2.pack()
        self.trocar.pack()

    def trocarTurmas(self):
        x = self.controller.getLinha()
        print("trocar a turma", self.listaTurmas.get(),"com", self.listaTurmas2.get())

    def setQualidadeBefore(self, qualidade):
        self.qualidadeBefore.set("Qualidade Inicial = {q: .5f}".format(q = qualidade))

    def setQualidadeAfter(self, qualidade):
        self.qualidadeAfter.set("Qualidade Otimizada = {q: .5f}".format(q = qualidade))

    def setDiferenca(self, a, b):
        self.diferenca.set("Melhora obtida foi de = {q: .3f}%".format(q = (b - a)/b *100))
    
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

