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
        self.listaTurmas  = ttk.Combobox(self.container, values = [
            "turma 1",
            "turma 2",
            "turma 3",
            "turma 4"
            ])
        self.listaTurmas2  = ttk.Combobox(self.container, values = [
            "turma 1",
            "turma 2",
            "turma 3",
            "turma 4"
            ])
        self.trocar = Button(self.container, text="Trocar",command=self.trocarTurmas)

    def setup_layout(self):
        self.listaTurmas.current(1)
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

