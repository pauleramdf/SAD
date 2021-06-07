import sqlalchemy
import pandas as pd

class Banco():    
    #Cria a conexao com o banco
    def __init__(self, parent):
        self.parent = parent
        self.engine = sqlalchemy.create_engine( 'mysql+pymysql://root:andre123@localhost:3306/salas')
        
        #Recebe o nome da tabela e
        #Retorna o data frame da tabela do banco.
    def lerTabela(self, tabela):
        df = pd.read_sql_table(tabela,self.engine)
        return df
    
        # Alimenta o banco com a tabela,
        #sobescreve caso já exista a tabela.
    def alimentarBanco(self, df, tabela, Bool):
        df.to_sql(
        name = tabela,
        con = self.engine,
        index = Bool,
        if_exists='replace'
    )

        #Transforma o dicionario das salas em um Data Frame.
    def salasDictToDF(self, salas):
        df = pd.DataFrame.from_dict(salas, orient='index').reset_index().rename(columns={'index': 'id_sala', 'cad': 'numero_cadeiras', 'acess':'acessivel', 'quali':'qualidade' })
        return df

        #Transforma o dicionario das turmas em um Data Frame.
    def turmasDictToDF(self, turmas):
        df = pd.DataFrame.from_dict(turmas, orient='index').reset_index().rename(columns={'index': 'id_turma', 'prof': 'professor', 'horario':'dias_horario','alunos' :'numero_alunos', "acess":'acessibilidade', 'quali':'qualidade' })
        return df

        #Cria o Data Frame dos dias da Semana.
    def diasSemanaToDF(self):
        dSemana = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab']
        df = pd.DataFrame(dSemana).rename(columns={0:'dia_semana'})
        return df

        #Cria o Data Frame dos horarios.
    def horario(self):
        horario = (1,2,3,4,5,6,7,8)
        df = pd.DataFrame(horario).rename(columns={0:'horario'})
        return df
    
        #Transforma o Data Frame das turmas em um dicionario.
    def turmasDF_toDict(self,df):
        turmasDf = list(df.drop('index',axis='columns').to_dict().items())
        turmas = {}
        for i in range (len(turmasDf[0][1])):
            turmas[i] = {"disciplina": turmasDf[0][1][i],"prof": turmasDf[1][1][i], "horario": transformaHorario(turmasDf[2][1][i]),
                 "alunos": int(turmasDf[3][1][i]), "curso": turmasDf[4][1][i], 
                 "periodo": int(turmasDf[5][1][i]), "acess": int(turmasDf[6][1][i]), "quali": int(turmasDf[7][1][i])}
        return turmas
    
        #Transforma o Data Frame das salas em um dicionario.
    def salasDF_toDict(self,df):
        salasDf = list(df.to_dict().items())
        salas = {}
        id_Salas = []
        for i in range (len(salasDf[0][1])):
            salas[salasDf[0][1][i]] = {"cad": int(salasDf[1][1][i]), "acess": int(salasDf[2][1][i]), "quali": int(salasDf[3][1][i])}
            id_Salas.append(salasDf[0][1][i])
        return salas
    
        #Transforma o dicionario da solucao em um Data Frame.
    def solucaoToDF(self,solucao):
        solucao = list(solucao.items())
        df = []
        # Somente os horarios com aulas
        for i in range(len(solucao)):
            # loop que passa pelas salas
            for key,value in solucao[i][1].items():
                # Loop que passa pelos dias e seus valores
                # Key = seg, ter ... | Value = 1: idTurma, 2: 0 ...
                for chave, valor in value.items():
                    # Verifica se teve aula no dia.
                    # Caso sim escreve o horario e a turma.
                    if valor > 0:
                        df.append([solucao[i][0],key,chave,valor])
        df = pd.DataFrame(df).rename(columns={0:'id_sala', 1:'dia_semana',2:'horario',3:'id_turma'})
        return df
    
    def solucaoToList(self,solucao):
        df = solucao.values.tolist()
        return df
    
    def filtro(self,data,filtrado,filtro):
        df = data[data[filtrado] == filtro]
        return df

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
