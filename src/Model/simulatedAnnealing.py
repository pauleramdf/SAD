import csv
import math
import random
#import sqlalchemy
from decimal import Decimal
import copy 
#import pandas as pd
#from Model.BancoDeDados.banco import Banco


class Model:
    def __init__(self, controller, parent):
        self.controller = controller
        #self,pesoOcup,pesoAcess,pesoQuali,temp,fator
        self.turmas = {}
        self.salas = {}
        self.horarios = {}
        self.id_Salas = []
        self.horario = {}
        self.pesoOcup = 1
        self.pesoAcess = 1
        self.pesoQuali = 1
        self.sorted_salas = []
        self.sorted_turmas = []
        self.solucaoIngenua = {}
        self.otimizacao = {}
        self.tabelaResultado = []
        self.qAfter = 0
        self.qBefore = 0 
        self.taxaQuali = 0
        self.taxaAcess = 0
        self.taxaOcup = 0
        #self.banco = Banco(self)


    def setup(self):
        df = csv.DictReader(open(r"{path}".format(path = self.pathSalas),encoding='utf-8'))
        df1 = csv.DictReader(open(r"{path}".format(path = self.pathTurmas),encoding='utf-8'))
        x = 1

        for row in df1:
            self.turmas[x] = {"disciplina": row['disciplina'],"prof": row['professor'], "horario": self.transformaHorario(row['dias_horario']),
                         "alunos": int(row['numero_alunos']), "curso": row['curso'], 
                         "periodo": int(row['período']), "acess": int(row["acessibilidade"]), "quali": int(row["qualidade"])}
            x+=1
        for row in df:
            self.salas[row['id_sala']] = {"id_sala": row['id_sala'],"cad": int(row['numero_cadeiras']), "acess": int(row['acessivel']), "quali": int(row['qualidade'])}
            self.id_Salas.append(row['id_sala'])

        for sala in self.id_Salas:
           self.horarios[sala] =  { "seg":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 },
                                "ter":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 },
                                "qua":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 },
                                "qui":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 },
                                "sex":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 },
                                "sab":{1: 0, 2: 0, 3: 0, 4: 0, 5: 0 , 6: 0 , 7: 0 , 8: 0 }}

        self.sorted_salas = sorted(self.salas.items(), key=lambda sala: (sala[1]['acess'],sala[1]['cad']), reverse=True)

        self.sorted_turmas = sorted(self.turmas.items(), key=lambda turma: (turma[1]['acess'], turma[1]['alunos']), reverse=True) 


    def solucao(self, pesos, temp, fator, maxIterations, pathTurmas, pathSalas):
        pesos = pesos.split(",")
        self.pesoOcup = Decimal(pesos[0])
        self.pesoAcess = Decimal(pesos[1])     
        self.pesoQuali = Decimal(pesos[2])
        self.pathTurmas = pathTurmas
        self.pathSalas = pathSalas
        self.temp = Decimal(temp)
        self.fator = Decimal(fator)
        self.maxIterations = int(maxIterations)

        self.setup()
        self.solucaoIngenua = self.alocaTurmasIngenua(self.horarios, self.sorted_turmas, self.sorted_salas)
        qBefore = self.qualidadeDaSolucao(self.solucaoIngenua)

        #otimiza a solução inicial utilizando a solução inicial e passando os parametros:
        #solInicial, turmas, salas, temperatura, n de iterações, 
        # e por ultimo o fator de resfriamento da temp(entre 0 e 1)
        self.otimizacao = self.simulatedAnnealing (self.solucaoIngenua, 
                                                    self.turmas, 
                                                    self.salas, 
                                                    Decimal(self.temp), 
                                                    self.maxIterations, 
                                                    Decimal(self.fator))

        qAfter = self.qualidadeDaSolucao(self.otimizacao)
        #print("a qualidade da slução otimizada é ",qualidade)
        #exibeSolucao(list(x.items()), turmas, salas)
        return (qBefore,qAfter)

    #transforma o horario para um formato mais amigavel
    def transformaHorario(self, horario):
        list = []
        turmaTemp = horario.split("-")
        for i in range(len(turmaTemp)):
            dia = int(turmaTemp[i][0])
            turno = turmaTemp[i][1]
            horarioIni = int(turmaTemp[i][2])
            if(turno == 'M'):
                horarioIni = 1 + horarioIni/2 
            if(turno == 'T'):
                horarioIni = 4 + horarioIni/2 
            elif(turno == 'N'):
                horarioIni = 7 + horarioIni/2
            if(int(turmaTemp[i][0]) == 2):
                dia = 'seg' 
            elif(int(turmaTemp[i][0]) == 3):
                dia = 'ter'
            elif(int(turmaTemp[i][0]) == 4):
                dia = 'qua'
            elif(int(turmaTemp[i][0]) == 5):
                dia = 'qui'
            elif(int(turmaTemp[i][0]) == 6):
                dia = 'sex'
            else:
                dia = 'sab'
            list.append((dia,int(horarioIni)))
        return list

    def getHorarioTurma(self, id_turma):
        id_turma = int(id_turma)
        return self.turmas[id_turma]['horario']

    def listaSalasPossiveis(self, id_turma):
        id_turma = int(id_turma)
        salasPossiveis = self.achaSalasPossiveis(self.turmas[id_turma], self.sorted_salas)
        return salasPossiveis

    def achaSalasPossiveis(self, turma, salas):
        #busca as salas que ainda estão livr
        salasPossiveis = {}
        for sala in salas:
            # Verifica a acessibilidade e o tamanho da turma. Ex:
            # Acess = 0 retornar turmas com acess 0 e 1
            # Acess = 1 retornar turmas com acess 1
            if(sala[1]['cad'] >= turma['alunos'] and sala[1]['acess'] >= turma['acess']):
                salasPossiveis[sala[0]] = {"cad": int(sala[1]['cad']), "acess": int(sala[1]['acess']), "quali": int(sala[1]['quali'])}
                
        salas = sorted(salasPossiveis.items(), key=lambda sala: (sala[1]['acess'],sala[1]['cad']))
        # print(salas)
        return salas

    def achaSalasDisponiveis(self, solucao, turma, salas):
        sol = solucao.copy()
        salasPossiveis = self.achaSalasPossiveis(turma, salas)
        h = turma['horario']
        #recebe a lista de horarios dessa turma
        salasDisponiveis = []
        #lista que recebe a solução
        for sala in salasPossiveis:
            for j in range(len(sol)):
                contador = 0
                for k in range(len(h)):
                    dia = h[k][0]
                    #recebe o dia do horario k 
                    horario = h[k][1] 
                    #recebe a hora do horario k
                    if(sol[sala[0]][dia][horario] == 0): 
                        contador += 1 
                        #se o horario estiver disponivel é incrementado este contador
            if(contador == len(h)): 
                #se o contador chegar ao mesmo tamanho da lista de horario, significa que essa 
                # sala está livre em todos os horarios dessa turma, logo ela pode ser alocada.
                salasDisponiveis.append(sala) #adiciona a sala avaliada na lista resultado
        return salasDisponiveis


    def alocaTurmasIngenua(self, horarios, turmas, salas):
        salasDisponiveis = []
        for turma in turmas:
            h = turma[1]['horario']
            salasDisponiveis = self.achaSalasDisponiveis(horarios, turma[1], salas)
            #print(salasDisponiveis)
            if(salasDisponiveis == []):
                print("deu conflito rs", turma[1]['alunos'])
            else:
                for i in range(len(h)):
                    dia = h[i][0] 
                    #recebe o dia do horario k 
                    horario = h[i][1] 
                    #recebe a hora do horario k
                    sala = salasDisponiveis[0][0]
                    #print("sala escolhida para alocação ", sala)
                    horarios[sala][dia][horario] = turma[0] #coloca o id(lista não ordenada) da turma no horario.
                    
        return horarios

        #calcula a taxa de ocupação de uma sala em relação a uma turma
    def taxaOcupacao(self,turma, sala):
        return Decimal(turma['alunos']) /sala['cad']

    #retorna 1 caso a sala esteja em uma sala de qualidade adequada
    #e retorna 0 caso contrario
    def taxaQualidade(self,turma, sala):
        if sala['quali'] >= turma['quali']:
            return 1
        return 0

    #retorna 1 caso a sala esteja em uma sala de acessibilidade adequada
    #e retorna 0 caso contrario
    def taxaAcessibilidade(self,turma, sala):
        if (sala['acess'] >= turma['acess']):
            return 1
        return 0

        #analisa qualidade da solução atual
    def analisaQualidade(self, a, turmas, salas):
        somatorio = []
        for sala in salas:
            # loop que passa pelas salas
            for dia in a[sala]:
                for h in range(8):
                    id_turma = a[sala][dia][h+1]
                    if id_turma > 0:
                        ocup = self.taxaOcupacao(turmas[id_turma], salas[sala])
                        quali = self.taxaQualidade(turmas[id_turma], salas[sala])
                        acess = self.taxaAcessibilidade(turmas[id_turma], salas[sala]) 
                        obj = {"ocup": ocup,"acess": acess ,"quali": quali}
                        somatorio.append(obj)
        return somatorio        
    def updateQualidade(self):
        self.qBefore = self.qualidadeDaSolucao(self.solucaoIngenua)
        self.qAfter = self.qualidadeDaSolucao(self.otimizacao)
        
    def qualidadeDaSolucao(self, solucao):
        erros = self.analisaQualidade(solucao, self.turmas, self.salas)
        sumOcup, sumQuali, sumAcess = (0,0,0)

        for erro in erros:
            sumOcup += Decimal(erro['ocup'])
            sumAcess += Decimal(erro['acess'])
            sumQuali += Decimal(erro['quali'])
        
        self.taxaQuali = Decimal(sumQuali/len(erros))
        self.taxaAcess = Decimal(sumAcess/len(erros))
        self.taxaOcup = Decimal(sumOcup/len(erros))

        sumQuali = Decimal(sumQuali/len(erros))*self.pesoQuali 
        sumAcess = Decimal(sumAcess/len(erros))*self.pesoAcess  
        sumOcup  = Decimal(sumOcup/len(erros))*self.pesoOcup
        return Decimal(sumQuali + sumOcup +sumAcess)/(self.pesoAcess + self.pesoOcup + self.pesoQuali)

    def trocarTurma(self, salas, dia, horario):
        self.solucaoIngenua = copy.deepcopy(self.otimizacao)
        self.otimizacao[salas[0]][dia][horario], self.otimizacao[salas[1]][dia][horario] = self.otimizacao[salas[1]][dia][horario], self.otimizacao[salas[0]][dia][horario]

    def trocaTurmas(self, a, numeroDeTrocas):
        temp = a.copy()
        achou = False
        for i in range(numeroDeTrocas+1):
            turma = random.choice(self.sorted_turmas)
            id_turma = turma[0]
            horarioTurma = turma[1]['horario']
            salasDisponiveis = self.achaSalasDisponiveis(temp, turma[1], self.sorted_salas)
            salasPossiveis = self.achaSalasPossiveis(turma[1], self.sorted_salas)

            if(len(salasDisponiveis) == 0):
                print("não ha salas disponiveis para troca")
                continue
            randomSala = random.choice(salasDisponiveis)
            for sala in salasPossiveis:
                for h in horarioTurma:
                    achou = True 
                    dia = h[0] 
                    hora = h[1]
                    if(temp[sala[0]][dia][hora] == id_turma):
                        temp[sala[0]][dia][hora]  = 0
                        temp[randomSala[0]][dia][hora] = id_turma
                if(achou):
                    achou = False
                    break
        return temp  

    def simulatedAnnealing (self, solucao, turmas, salas, temp, maxIterations, alfa):
        inicial = copy.deepcopy(solucao)
        probabilidade = 0
        erro = 0
        qualiSolucao = self.qualidadeDaSolucao(inicial)
        qSolucao = self.qualidadeDaSolucao(solucao)
        
        while (temp >= 2):
            numeroDeTrocas = int(math.log2(temp))
            for i in range(maxIterations):       
                qualidadeInicial = self.qualidadeDaSolucao(inicial)
                sucessor = self.trocaTurmas(copy.deepcopy(inicial), numeroDeTrocas)
                qualidadeSucessor = self.qualidadeDaSolucao(sucessor)
                #print("temperatura",temp,"qualidade da solucao", qualidadeInicial, qualidadeSucessor, "probabilidade", probabilidade, "erro:",  qualidadeInicial - qualidadeSucessor)
                if(qualidadeSucessor > qualidadeInicial):
                    #print("trocou aqui")
                    inicial = copy.deepcopy(sucessor)
                else:
                    erro = abs(Decimal(qualidadeInicial) - Decimal(qualidadeSucessor))
                    probabilidade = math.exp(Decimal(-erro/temp))
                    n = random.random()
                    if(n <= probabilidade):
                        init = copy.deepcopy(sucessor)
                        qualidadeInicial = qualidadeSucessor

            i = 0 
            temp = temp * alfa 
        if(qualidadeInicial > qSolucao ):
            return inicial                     
        else: 
            return solucao

    def exibeSolucao(self, solucao):
        temp = list(solucao.items())
        self.tabelaResultado = []
        for i in range(len(temp)):
            for key,value in temp[i][1].items():
                teveAula = False
                for chave, valor in value.items():
                    if valor > 0:
                        teveAula = True
                        lista = []
                        lista.append(temp[i][0])
                        lista.append(key)
                        lista.append(chave)
                        lista.append(self.turmas[valor]['disciplina'])
                        lista.append(valor)
                        self.tabelaResultado.append(lista)

        return self.tabelaResultado

'''        
    def salvarSolucao(self):
        df = self.banco.solucaoToDF(self.otimizacao)
        self.banco.alimentarBanco(df,"solucao", False)
''' 
