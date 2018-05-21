# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
"""
Algoritmos y Estructuras de Datos
Proyecto Final
Antonio Reyes #17273
Esteban Cabrera #17781
Miguel #17102
"""
import xlrd
file_location = "C:/Users/Antonio/Desktop/ProyectoFinal/Database.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474",username="neo4j", password="1111")

dataB = db.labels.create("Database")
gen = db.labels.create("Genero")

#se crea un diccionario (como vimos en hashmaps)
#database = {}
#databaseNAME = {}

#en el for se puede poner sheet.nrows para imprimir todo

for x in range(sheet.nrows):
    name = sheet.cell_value(x,0)
    gen1 = sheet.cell_value(x,1)
    gen2 = sheet.cell_value(x,2)
    gen3 = sheet.cell_value(x,3)

    #generos = []

    unidad = db.nodes.create(nombre=name, genero1=gen1, genero2=gen2, genero3=gen3)
    dataB.add(unidad)

    try:
        unidad.relationships.create("contains", gen.get(genero=gen1)[0])
    except Exception:
        genNode = db.nodes.create(genero=gen1)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen1)[0])

    try:
        unidad.relationships.create("contains", gen.get(genero=gen2)[0])
    except Exception:
        genNode = db.nodes.create(genero=gen2)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen2)[0])

    try:
        unidad.relationships.create("contains", gen.get(genero=gen3)[0])
    except Exception:
        genNode = db.nodes.create(genero=gen3)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen3)[0])

    
    
    

print ("Done :v")
    
#imprime todo el database
#for key, value in database.iteritems() :
#    print key, value


