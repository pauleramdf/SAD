import csv
import math
import random
import sqlalchemy
from decimal import Decimal
import copy 
from Model.BancoDeDados.banco import Banco


class Model:
    def __init__(self, controller, parent):
        self.controller = controller
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
        self.reverterSolucao = {}
        self.otimizacao = {}
        self.tabelaResultado = []
        self.qInicial = 0
        self.qAfter = 0
        self.qBefore = 0 
        self.taxaQuali = 0
        self.taxaAcess = 0
        self.taxaOcup = 0
        self.banco = Banco(self)

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

    #Inicia a otimização da solucao
    def solucao(self, pesos, temp, fator, maxIterations, pathTurmas, pathSalas):
        #configura os parametros para começar a otimização
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

        self.reverterSolucao = copy.deepcopy(self.otimizacao)
        self.qInicial = qAfter

        return (qBefore,qAfter)

    #Recebe uma String que representa o horario da turma e transforma esse 
    # horario em um formato mais amigavel. 
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

    #Busca o horario de uma turma com base em seu id
    def getHorarioTurma(self, id_turma):
        id_turma = int(id_turma)
        return self.turmas[id_turma]['horario']

    #Busca as salas possiveis para um dado id de turma
    def listaSalasPossiveis(self, id_turma):
        id_turma = int(id_turma)
        salasPossiveis = self.achaSalasPossiveis(self.turmas[id_turma], self.sorted_salas)
        return salasPossiveis

    #Essa função recebe uma lista de salas e uma turma. 
    #Ela percorre todas as salas nessa lista e procura as salas que obedecem as 
    #restrições Hard do problema, e retorna somente estas salas.
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

    #Essa funçao recebe o solução, uma turma e a lista de salas e retorna uma lista de salas.
    #Ela percorre o resultado de "salasPossiveis", e checa se essa sala está livre no horario
    #da Turma passada como parametro. É retornada a lista de salas que estão livres.
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

    #Faz uma alocação "burra", escolhendo sempre a primeira sala entre as salas disponiveis para a turma
    def alocaTurmasIngenua(self, horarios, turmas, salas):
        salasDisponiveis = []
        for turma in turmas:
            h = turma[1]['horario']
            salasDisponiveis = self.achaSalasDisponiveis(horarios, turma[1], salas)
            #print(salasDisponiveis)        
            if(salasDisponiveis == []):
                #print("deu conflito", turma[1]['alunos'])
                continue
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

    # Essa função percorre todas as salas e, caso alocadas para uma turma, calcula 
    # as respectivas taxas de qualidade para essa turma dentro dessa sala.
    # essa função retorna as taxas de cada uma das salas alocadas.
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

    #atualiza o valor qualidade das soluções armazenadas
    def updateQualidade(self):
        self.qBefore = self.qualidadeDaSolucao(self.solucaoIngenua)
        self.qAfter = self.qualidadeDaSolucao(self.otimizacao)

    # Calcula a qualidade geral da solução com base em 3 taxas e seus respecitvos pesos.
    # Taxa de Ocupação das salas, Taxa de Qualidade das salas, e Taxa de acessibilidade. 
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
    
    #Recebe duas salas e uma turma. Então troca essa turma de uma sala para a outra.
    #Caso a sala destino quebre alguma restrição hard, um erro é exibido para o usuario.
    #Caso contrario, a troca é realizada e a solução é atualizada
    def trocarTurma(self, salas, dia, horario):
        achou = False
        if self.otimizacao[salas[1]][dia][horario] == 0 or (salas[0] in self.listaSalasPossiveis(self.otimizacao[salas[1]][dia][horario])):
            self.solucaoIngenua = copy.deepcopy(self.otimizacao)
            self.otimizacao[salas[0]][dia][horario], self.otimizacao[salas[1]][dia][horario] = self.otimizacao[salas[1]][dia][horario], self.otimizacao[salas[0]][dia][horario]
        else:
            raise Exception("Sala destino não respeita as restrições da turma")


    #Procura entre as salas disponiveis para uma determinada turma, qual delas tem a melhor taxa qualidade.
    #Retorna a sala que tem maior qualidade, ou seja, a sala que melhor se adequa a turma. 
    def achaMelhorSala(self, turma, salas):
        somatorio = []
        for (id_sala,value) in salas:
            # loop que passa pelas salas
            ocup = self.taxaOcupacao(turma, value)
            quali = self.taxaQualidade(turma, value)
            acess = self.taxaAcessibilidade(turma, value) 
            soma = (ocup*self.pesoOcup + acess*self.pesoAcess + quali*self.pesoQuali)/(self.pesoOcup + self.pesoAcess + self.pesoQuali)
            somatorio.append((id_sala,soma))

        melhor = sorted(somatorio, key = lambda sala: sala[1],reverse=True)     
        return melhor[0][0]
    
    #recebe uma solução e a quantidade de trocas de turmas de salas que devem ser feitas
    def trocaTurmas(self, a, numeroDeTrocas):
        temp = a.copy()
        achou = False
        for i in range(numeroDeTrocas+1):
            #A cada iteração uma nova turma é sorteada para a troca
            turma = random.choice(self.sorted_turmas)
            id_turma = turma[0]
            horarioTurma = turma[1]['horario']
            #são buscadas salas vazias que correspondem as restrições hard dessa turma sorteada
            salasDisponiveis = self.achaSalasDisponiveis(temp, turma[1], self.sorted_salas)
            salasPossiveis = self.achaSalasPossiveis(turma[1], self.sorted_salas)

            #caso não exista sala vazia para essa turma nesse respectivo horario, não é feita nenhuma troca.
            if(len(salasDisponiveis) == 0):
                #print("não ha salas disponiveis para troca")
                continue
            
            #é sorteada uma sala dentre as salas vazias. Então essa turma troca sua atual sala por essa sala vazia.
            #randomSala = random.choice(salasPossiveis)
            melhorSala = self.achaMelhorSala(turma[1], salasDisponiveis)
            for sala in salasPossiveis:
                for h in horarioTurma:
                    achou = True 
                    dia = h[0] 
                    hora = h[1]
                    if(temp[sala[0]][dia][hora] == id_turma):
                        temp[sala[0]][dia][hora]  = 0
                        temp[melhorSala][dia][hora] = id_turma
                if(achou):
                    achou = False
                    break
        return temp  

    #Recebe uma solução inicial, o dicionario de turmas e salas, a temperatura inicial,
    #a quantidade maxima de iterações por temperatura, e o fator de resfriamento.
    #São feitas diversas modições na solução inicial enquanto a temperatura esfria.
    #A cada iteração são feitas n trocas na solução inicial, sendo n = log2(temperatura).
    #As trocas são feitas de forma aleatoria entre as salas que respeitam as condições "hard" 
    #da respectiva turma.
    #Caso a qualidade da solução modificada seja melhor que a solução inicial, nos trocamos
    #de solução. Caso contrario é calculado uma probabilidade de realizar a troca entre as turmas.
    #Quanto maior a diferença de qualidade entre as turmas, maior é chance de realizar essa troca
    # mesmo que a qualidade seja inferior.
    #A otimização termina quando a temperatura for igual ou inferior a 2.
    #Então a qualidade da solução obtida atraves da otimização é comparada com a solução incial.
    #É retornada a solução que obteve maior qualidade.
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
                #Confere se a qualidade da solução melhorou apos a troca ou não.
                #Caso seja maior, então essa nova solução é assumida.
                if(qualidadeSucessor > qualidadeInicial):
                    inicial = copy.deepcopy(sucessor)
                else:
                    #calcula a probabilidade de realizar a troca mesmo que a qualidade seja inferior
                    erro = abs(Decimal(qualidadeInicial) - Decimal(qualidadeSucessor))
                    probabilidade = math.exp(Decimal(-erro/temp))
                    n = random.random()
                    if(n <= probabilidade):
                        init = copy.deepcopy(sucessor)
                        qualidadeInicial = qualidadeSucessor

            i = 0 
            #atualização da temperatura baseada no fator de resfriamento
            temp = temp * alfa 
        #compara a qualidade inicial com a qualidade da otimização
        if(qualidadeInicial > qSolucao ):
            return inicial                     
        else: 
            return solucao

    #Transforma o dicionario onde a solução está armazenada em uma lista para ser exibida na tabela
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

    #Descarta todas as alterações feitas até então carregando a solução salva no banco de dados 
    #ou obtida atraves do simulatedAnnealing
    def reverterAlteracoes(self):
        self.solucaoIngenua = self.otimizacao
        self.otimizacao = self.reverterSolucao
        self.qAfter = self.qInicial
        self.updateQualidade()

    #Salva a solução otimizada no banco de dados 
    def salvarSolucao(self):
        df = self.banco.solucaoToDF(self.otimizacao)
        turmas = self.banco.turmasDictToDF(self.turmas)
        salas = self.banco.salasDictToDF(self.salas)
        self.banco.alimentarBanco(turmas, 'turmas', False)
        self.banco.alimentarBanco(salas, 'salas', False)
        self.banco.alimentarBanco(df,"solucao", False)

    #Carrega uma solução salva no banco de dados, assim como os dicionarios de turmas e salas dessa solução
    def carregarSolucao(self):
        turmas = self.banco.lerTabela('turmas')
        salas = self.banco.lerTabela('salas')
        self.turmas = self.banco.turmasDF_toDict(turmas)
        self.salas = self.banco.salasDF_toDict(salas)
        df = self.banco.lerTabela('solucao')
        self.otimizacao = self.banco.solucaoToDict(df)
        df = self.banco.solucaoToList(df)
        self.sorted_salas = sorted(self.salas.items(), key=lambda sala: (sala[1]['acess'],sala[1]['cad']), reverse=True)
        self.sorted_turmas = sorted(self.turmas.items(), key=lambda turma: (turma[1]['acess'], turma[1]['alunos']), reverse=True) 
        self.solucaoIngenua = self.otimizacao
        self.reverterSolucao = copy.deepcopy(self.otimizacao)
        return df
