import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

class Filtros(Frame):
    def __init__(self, container, parent, flag):
        self.container = container
        self.parent = parent
        self.flag = flag
        self.frm = Frame(self.container, bg = "grey",relief=RIDGE)
        self.frm.pack(side=TOP)

        self.texto1 = StringVar()
        self.makewidgets()
        

    def makewidgets(self): 
        self.create_widgets() 
        self.setup_layout()

    def create_widgets(self):
        self.label = Label(self.frm, text="Escolha a caracteristica que deseja filtrar", bg = "grey", anchor=CENTER, fg="black")
        self.label1 = Label(self.frm, text="Item", bg = "grey", anchor=CENTER, fg="black")
        
        self.listaFiltros = ttk.Combobox(self.frm, justify=CENTER, 
            values = ["Filtros"])
        self.entrada = Entry(self.frm, textvariable=self.texto1, width = 25)
        self.button = Button(self.frm, text="Buscar",command=self.buscar)

    def setup_layout(self):
        lista = []
        self.listaFiltros.current(0)
        self.label.pack(side=LEFT, padx=(5,5),  pady=(2,2))
        self.listaFiltros.pack(side=LEFT, padx=(5,5),  pady=(2,2))
        self.label1.pack(side=LEFT, padx=(5,5),  pady=(2,2))
        self.entrada.pack(side=LEFT, padx=(5,5), pady=(2,2))
        self.button.pack(side=LEFT, padx=(5,5), pady=(2,2))

        if(self.flag == 1):
            filtros = ["ID",'disciplina','professor','horario', 'alunos','curso','periodo','acessibilidade','qualidade']
        else:
            filtros = ["ID",'cadeiras','acessibilidade','qualidade']

        for filtro in filtros:
            lista.append(filtro)
            self.listaFiltros['values'] = lista

    def buscar(self):
        entrada = self.entrada.get()
        filtro = self.listaFiltros.get()
        self.parent.buscar(entrada, filtro)


class Items(Frame):
    def __init__(self, container, parent, flag):
        self.container = container
        self.parent = parent
        self.flag = flag

        self.frm = Frame(self.container, bg = "black",relief=RIDGE)
        self.frm.pack(side=LEFT,expand=YES, fill=BOTH)
        self.makewidgets()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )

        style.map('Treeview', 
            background=[('selected', 'blue')])

    def makewidgets(self):
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        if(self.flag == 1):
            self.tabela = ttk.Treeview(self.frm, columns=('id', 'disciplina', 'professor', 'horario', 'alunos', 'curso',
                                                            'periodo', 'acessibilidade','qualidade'), show='headings')

            self.tabela.column('id', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('disciplina', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('professor', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('horario', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('alunos', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('curso', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('periodo', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('acessibilidade', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('qualidade', minwidth=0, width=30, anchor=CENTER)

            self.tabela.heading('id',text='ID')
            self.tabela.heading('disciplina',text='DISCIPLINA')
            self.tabela.heading('professor',text='PROFESSOR')
            self.tabela.heading('horario',text='HORARIO')
            self.tabela.heading('alunos',text='ALUNOS')
            self.tabela.heading('curso',text='CURSO')
            self.tabela.heading('periodo',text='PERIODO')
            self.tabela.heading('acessibilidade',text='ACESSIBILIDADE')
            self.tabela.heading('qualidade',text='QUALIDADE')

        else:
            self.tabela = ttk.Treeview(self.frm, columns=('id', 'cadeiras','acessibilidade','qualidade'), show='headings')        
            self.tabela.column('id', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('cadeiras', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('acessibilidade', minwidth=0, width=30, anchor=CENTER)
            self.tabela.column('qualidade', minwidth=0, width=30, anchor=CENTER)

            self.tabela.heading('id',text='ID')
            self.tabela.heading('cadeiras',text='CADEIRAS')
            self.tabela.heading('acessibilidade',text='ACESSIBILIDADE')
            self.tabela.heading('qualidade',text='QUALIDADE')
        
        self.sbar = Scrollbar(self.frm)
        self.sbar.config(command= self.tabela.yview) 
        self.tabela.config(yscrollcommand=self.sbar.set)
    
    def setup_layout(self):
        self.sbar.pack(side=RIGHT, fill=Y) 
        self.tabela.pack(side=LEFT, expand=YES, fill=BOTH)
    
    def updateTabela(self, texto):
        if(self.flag == 1):
            for record in self.tabela.get_children():
                self.tabela.delete(record)
            for (x1,x2,x3,x4,x5,x6,x7,x8,x9) in texto:
                self.tabela.insert("","end",values=(x1,x2,x3,x4,x5,x6,x7,x8,x9))
        else:
            for record in self.tabela.get_children():
                self.tabela.delete(record)
            for (x1,x2,x3,x4) in texto:
                self.tabela.insert("","end",values=(x1,x2,x3,x4))


    def setTabela(self, texto): 
        if(self.flag == 1):
            for (x1,x2,x3,x4,x5,x6,x7,x8,x9) in texto:
                self.tabela.insert("","end",values=(x1,x2,x3,x4,x5,x6,x7,x8,x9))
        else:
            for (x1,x2,x3,x4) in texto:
                self.tabela.insert("","end",values=(x1,x2,x3,x4))

class Busca:
    def __init__(self, controller, turmas, salas, flag):
        self.controller = controller
        self.turmas = turmas
        self.salas = salas
        self.flag = flag
        self.filtros = None
        self.items = None

    def iniciaTabela(self):
        resultado = []
        if(self.flag == 1):
            aux = list(self.turmas.items())
            for key, value in aux:
                resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                    value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])
        else:
            aux = list(self.salas.items())
            for key, value in aux:
                resultado.append([key, value['cad'], value['acess'], value['quali']])

        self.items.setTabela(resultado)

    def inicia(self):
        root = Tk()
        WIDTH = 700
        HEIGHT = 400
        root.title("Busca")
        root.geometry("%sx%s" % (WIDTH, HEIGHT))

        self.filtros = Filtros(root, self, self.flag)
        self.items = Items(root, self, self.flag)
        self.iniciaTabela()
        root.mainloop()

    def buscar(self, entrada, filtro):
        try:
            resultado = []
            if(self.flag == 1): 
                aux = list(self.turmas.items())
                if(filtro == "ID"):
                    for key, value in aux:
                        if(key == int(entrada)):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])
                elif(filtro == "disciplina"):
                    for key, value in aux:
                        if(value['disciplina'] == entrada):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                elif(filtro == "professor"):
                    for key, value in aux:
                        if(value['prof'] == entrada):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                elif(filtro == "horario"):
                    for key, value in aux:
                        if(value['horario'] == entrada):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                elif(filtro == "alunos"):
                    for key, value in aux:
                        if(value['alunos'] == int(entrada)):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                elif(filtro == "curso"):
                    for key, value in aux:
                        if(value['curso'] == entrada):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                elif(filtro == "periodo"):
                    for key, value in aux:
                        if(value['periodo'] == int(entrada)):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])
                
                elif(filtro == "acessibilidade"):
                    for key, value in aux:
                        if(value['acess'] == int(entrada)):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])
                
                elif(filtro == "qualidade"):
                    for key, value in aux:
                        if(value['quali'] == int(entrada)):
                            resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])

                else:
                    for key, value in aux:
                        resultado.append([key, value['disciplina'], value['prof'], value['horario'], 
                            value['alunos'], value['curso'], value['periodo'], value['acess'], value['quali']])
            else:
                aux = list(self.salas.items())
                if(filtro == "ID"):
                    for key, value in aux:
                        if(key == entrada):
                            resultado.append([key, value['cad'], value['acess'], value['quali']])
                if(filtro == "cadeiras"):
                    for key, value in aux:
                        if(value['cad'] == int(entrada)):
                            resultado.append([key, value['cad'], value['acess'], value['quali']])
                if(filtro == "acessibilidade"):
                    for key, value in aux:
                        if(value['acess'] == int(entrada)):
                            resultado.append([key, value['cad'], value['acess'], value['quali']])
                if(filtro == "qualidade"):
                    for key, value in aux:
                        if(value['quali'] == int(entrada)):
                            resultado.append([key, value['cad'], value['acess'], value['quali']])
                
            self.items.updateTabela(resultado)
        except:
           messagebox.showinfo(title="ERRO", message="Busca Invalida")
           self.quit()


