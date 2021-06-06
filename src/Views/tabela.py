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

class Tabela(Frame):
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent

        self.frm = Frame(parent, bg = "black",relief=RIDGE)
        self.frm.pack(side=LEFT,expand=YES, fill=BOTH)
        self.makewidgets()

    def makewidgets(self):
        self.sbar = Scrollbar(self.frm)
        self.tabela = ttk.Treeview(self.frm, columns=('id sala','dia','horario','cod turma','id turma'), show='headings')
        self.sbar.config(command= self.tabela.yview) 

        self.tabela.config(yscrollcommand=self.sbar.set)
        self.tabela.column('id sala', minwidth=0, width=30)
        self.tabela.column('dia', minwidth=0, width=30)
        self.tabela.column('horario', minwidth=0, width=30)
        self.tabela.column('cod turma', minwidth=0, width=30)
        self.tabela.column('id turma', minwidth=0, width=30)

        self.tabela.heading('id sala',text='ID SALA')
        self.tabela.heading('dia',text='DIA')
        self.tabela.heading('horario',text='HORARIO')
        self.tabela.heading('cod turma',text='COD TURMA')
        self.tabela.heading('id turma',text='ID TURMA')

        self.sbar.pack(side=RIGHT, fill=Y) 
        self.tabela.pack(side=LEFT, expand=YES, fill=BOTH)

    def settext(self, texto):
        #self.text.delete('1.0', END) 
        #self.text.insert('1.0', texto) 
        for (s,d,h,t,i) in texto:
            self.tabela.insert("","end",values=(s,d,h,t,i))

    def getLinha(self):
        try:
            linhaSelecionada = self.tabela.selection()[0]
            valores = self.tabela.item(linhaSelecionada, "values")
            return valores
        except:
            messagebox.showinfo(title="ERRO", message="Selecione uma linha valida")