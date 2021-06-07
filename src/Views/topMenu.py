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

class TopMenu(Frame):
    def __init__(self, controller, parent):

        self.controller = controller
        self.parent = parent
        self.frm = Frame(parent, bg = "grey",relief=RIDGE)
        self.frm.pack(side=TOP)

        self.texto1 = StringVar()
        self.texto2 = StringVar()
        self.texto3 = StringVar()
        self.texto4 = StringVar()
        self.texto5 = StringVar()
        self.texto6 = StringVar()
        self.makewidgets()
        

    def makewidgets(self): 

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.label = Label(self.frm, text="Insira os parametros\npara começar a\notimização da alocação", bg = "grey", anchor=CENTER, fg="black", width = 20)
        self.label1 = Label(self.frm, text="Pesos", bg = "grey", fg="black")
        self.label2 = Label(self.frm, text="Temperatura", bg = "grey", fg="black")
        self.label3 = Label(self.frm, text="Fator de resfriamento", bg = "grey", fg="black")
        self.label4 = Label(self.frm, text="Max Iterações", bg = "grey", fg="black")
        self.label5 = Label(self.frm, text="Caminho Turmas", bg = "grey", fg="black")
        self.label6 = Label(self.frm, text="Caminho Salas", bg = "grey",  fg="black")

        self.texto1.set("1 1 1")
        self.texto2.set("1000")
        self.texto3.set("0.90")
        self.texto4.set("10")
        self.texto5.set("C:/Users/Paulo/Desktop/TrabalhoSAD/cenario1-turmas.csv")
        self.texto6.set("C:/Users/Paulo/Desktop/TrabalhoSAD/cenario1-salas.csv")
        self.entrada1 = Entry(self.frm, textvariable=self.texto1, width = 25)
        self.entrada2 = Entry(self.frm, textvariable=self.texto2, width = 25)
        self.entrada3 = Entry(self.frm, textvariable=self.texto3, width = 25)
        self.entrada4 = Entry(self.frm, textvariable=self.texto4, width = 25)
        self.entrada5 = Entry(self.frm, textvariable=self.texto5, width = 25)
        self.entrada6 = Entry(self.frm, textvariable=self.texto6, width = 25)

        self.button = Button(self.frm, text="Começar otimização",command=self.initSimulacao)

        self.button_turma = Button(self.frm,
                        text = "Browse Files",
                        command = lambda: self.browseFiles(True))

        self.button_sala = Button(self.frm,
                        text = "Browse Files",
                        command = lambda: self.browseFiles(False))


    def setup_layout(self):
        self.label.grid(row = 0, padx = (5,5),pady = (5,5))
        self.label1.grid(row = 1, column=0, padx = (5,5),pady = (5,5))
        self.label2.grid(row = 1, column=1, padx = (5,5),pady = (5,5))
        self.label3.grid(row = 1, column=2, padx = (5,5),pady = (5,5))
        self.label4.grid(row = 1, column=3, padx = (5,5),pady = (5,5))
        self.label5.grid(row = 1, column=4, padx = (5,5),pady = (5,5))
        self.label6.grid(row = 1, column=5, padx = (5,5),pady = (5,5))

        self.entrada1.grid(row = 2, column=0,padx = (5,5),pady = (5,5))
        self.entrada2.grid(row = 2, column=1,padx = (5,5),pady = (5,5))
        self.entrada3.grid(row = 2, column=2,padx = (5,5),pady = (5,5))
        self.entrada4.grid(row = 2, column=3,padx = (5,5),pady = (5,5))
        self.entrada5.grid(row = 2, column=4,padx = (5,5),pady = (5,5))
        self.entrada6.grid(row = 2, column=5,padx = (5,5),pady = (5,5))

        self.button.grid(row=3)
        self.button_turma.grid(row = 3, column = 4, padx = (5,5),pady = (5,5))
        self.button_sala.grid(row = 3, column = 5, padx = (5,5),pady = (5,5))
      
    def initSimulacao(self):
        self.texto1 = self.entrada1.get()
        self.texto2 = self.entrada2.get()
        self.texto3 = self.entrada3.get()
        self.texto4 = self.entrada4.get()
        self.texto5 = self.entrada5.get()
        self.texto6 = self.entrada6.get()
        self.controller.otimizacao_btn_pressed(
            self.texto1, 
            self.texto2, 
            self.texto3, 
            self.texto4,
            self.texto5,
            self.texto6)

    def browseFiles(self, turma):

            filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a File",
                                              filetypes = (("csv files",
                                                            ".csv"),
                                                           ("all files",
                                                            ".")))

            if turma:
                self.entrada5.delete(0,END)
                self.entrada5.insert(0,filename)
            else:
                self.entrada6.delete(0,END)
                self.entrada6.insert(0,filename)

