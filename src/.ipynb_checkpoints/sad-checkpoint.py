import csv

df = csv.DictReader(open("cenario1-salas.csv",encoding='uft-8'))


salas = {}
for row in df:
    print(row)
    salas[row['id_sala']] = {"cad": row['numero_cadeiras'], "acess": row['acessivel'], "quali": row['qualidade']}

print(salas)