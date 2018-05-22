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
file_location = "C:/Users/Antonio/Desktop/ProyectoFinal/prueba.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474",username="neo4j", password="1111")

dataB = db.labels.create("Database")
gen = db.labels.create("Genero")

#se crea un diccionario (como vimos en hashmaps)
database = {}


#donde se guardan los generos de las series que ya se vieron
historial = []

#en el for se puede poner sheet.nrows para imprimir todo
def add_Excel():
    for x in range(sheet.nrows):
        name = sheet.cell_value(x,0)
        gen1 = sheet.cell_value(x,1)
        gen2 = sheet.cell_value(x,2)
        gen3 = sheet.cell_value(x,3)

        generos = []

        generos.append(gen1)
        generos.append(gen2)
        generos.append(gen3)

        database[name] = generos

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


def add_database():
    name = raw_input("Ingresar nombre de la Película o Serie: ")
    gen1 = raw_input("Ingrese genero1: ")
    gen2 = raw_input("Ingrese genero2: ")
    gen3 = raw_input("Ingrese genero3: ")

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

    database[name] = [gen1,gen2,gen3]

def watch():
    name = raw_input("Ingrese el nombre de la Película o Serie: ")

    gen1 = database[name][0]
    gen2 = database[name][1]
    gen3 = database[name][2]

    
    historial.append(gen1)
    historial.append(gen2)
    historial.append(gen3)

    #print name + historial[0] + historial[1] + historial[2]


def menu():
    print("0. Agregar valores del documento Excel")
    print("1. Ingresar nueva Película/Serie a la base de datos")
    print("2. Ver Película o Serie")
    print("9. Salir")
    
    
menu()
opcion = input("Ingrese la acción a realizar")
print ("**********************************")
print ("**********************************")

while(opcion != 9):
    if(opcion == 0):
        add_Excel()
        print ("**********************************")
        print ("**********************************")
        print ("Base de datos agregada")
        menu()
        opcion = input("Ingrese la accion a realizar: ")
        
    elif(opcion == 1):
        add_database()
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Ingrese la accion a realizar: ")

    elif(opcion == 2):
        watch()
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Ingrese la accion a realizar: ")

    else:
        print("La opción ingresada no es valida")
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Ingrese la accion a realizar: ")

print ("Gracias por usar el programa")

