# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
"""
Algoritmos y Estructuras de Datos
Proyecto Final
Antonio Reyes #17273
Esteban Cabrera #17781
Miguel #17102
"""
import random
import xlrd
file_location = "C:/Users/Antonio/Desktop/Recommendation-System-python-neo4J-master/Database.xlsx"
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
    lista_gen = []
    for x in range(sheet.nrows):
        name = sheet.cell_value(x,0)
        gen1 = sheet.cell_value(x,1)
        gen2 = sheet.cell_value(x,2)
        gen3 = sheet.cell_value(x,3)

        lista_gen = []

        lista_gen.append(gen1)
        lista_gen.append(gen2)
        lista_gen.append(gen3)

        lista_gen.sort()

        gen1 = lista_gen[0]
        gen2 = lista_gen[1]
        gen3 = lista_gen[2]

        generos = []

        generos.append(gen1)
        generos.append(gen2)
        generos.append(gen3)

        database[name] = generos

        unidad = db.nodes.create(nombre=name, genero1=gen1, genero2=gen2, genero3=gen3)
        dataB.add(unidad)

        try:
            unidad.relationships.create("contains", gen.get(genero=gen1)[0])
            gen.get(genero=gen1)[0].relationships.create("contains", unidad)
        except Exception:
            genNode = db.nodes.create(genero=gen1)
            gen.add(genNode)
            unidad.relationships.create("contains", gen.get(genero=gen1)[0])
            gen.get(genero=gen1)[0].relationships.create("contains", unidad)

        try:
            unidad.relationships.create("contains", gen.get(genero=gen2)[0])
            gen.get(genero=gen2)[0].relationships.create("contains", unidad)
        except Exception:
            genNode = db.nodes.create(genero=gen2)
            gen.add(genNode)
            unidad.relationships.create("contains", gen.get(genero=gen2)[0])
            gen.get(genero=gen2)[0].relationships.create("contains", unidad)

        try:
            unidad.relationships.create("contains", gen.get(genero=gen3)[0])
            gen.get(genero=gen3)[0].relationships.create("contains", unidad)
        except Exception:
            genNode = db.nodes.create(genero=gen3)
            gen.add(genNode)
            unidad.relationships.create("contains", gen.get(genero=gen3)[0])
            gen.get(genero=gen3)[0].relationships.create("contains", unidad)


def add_database():
    listaOrden = []
    name = raw_input("Insert name: ")
    gen1 = raw_input("Insert genre1 ")
    gen2 = raw_input("Insert genre2: ")
    gen3 = raw_input("Insert genre3: ")

    listaOrden.append(gen1)
    listaOrden.append(gen2)
    listaOrden.append(gen3)

    listaOrden.sort()

    gen1 = listaOrden[0]
    gen2 = listaOrden[1]
    gen3 = listaOrden[2]

    unidad = db.nodes.create(nombre=name, genero1=gen1, genero2=gen2, genero3=gen3)
    dataB.add(unidad)

    try:
        unidad.relationships.create("contains", gen.get(genero=gen1)[0])
        gen.get(genero=gen1)[0].relationships.create("contains", unidad)
    except Exception:
        genNode = db.nodes.create(genero=gen1)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen1)[0])
        gen.get(genero=gen1)[0].relationships.create("contains", unidad)

    try:
        unidad.relationships.create("contains", gen.get(genero=gen2)[0])
        gen.get(genero=gen2)[0].relationships.create("contains", unidad)
    except Exception:
        genNode = db.nodes.create(genero=gen2)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen2)[0])
        gen.get(genero=gen2)[0].relationships.create("contains", unidad)

    try:
        unidad.relationships.create("contains", gen.get(genero=gen3)[0])
        gen.get(genero=gen3)[0].relationships.create("contains", unidad)
    except Exception:
        genNode = db.nodes.create(genero=gen3)
        gen.add(genNode)
        unidad.relationships.create("contains", gen.get(genero=gen3)[0])
        gen.get(genero=gen3)[0].relationships.create("contains", unidad)

    database[name] = [gen1,gen2,gen3]

def watch():
    name = raw_input("Insert name: ")

    try:
        query = "MATCH (n:Database) WHERE n.nombre='"+name+"' RETURN n.genero1, n.genero2, n.genero3"
        results = db.query(query, data_contents=True)
        a = results.rows
        for x in a:
            historial.append(x[0])
            historial.append(x[1])
            historial.append(x[2])




    except Exception:
        print("The movie or TV show you were looking for is not in the database, you can add it by going to option 1")

    popular_topics(name)

#se utiliza el cÃ³digo mostrado en este link para mostrar los generos que se repiten mÃ¡s veces
#https://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list
def popular_topics(name):
    nombre = name
    #diccionario que determinarÃ¡ cuales son los 5 generos mÃ¡s vistos
    top_5 = []
    #por cada genero en la lista....
    word_counter = {}
    for word in historial:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)

    top_5 = popular_words[:5]

    #se ordenan los generos en orden alfabetico
    lista = []
    print "Most watched genres: "
    for x in top_5:
        lista.append(x)
        print x

    print "We recommend: "
    print "-----------------"
    print "-----------------"
    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero1:'"+top_5[0]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero2:'"+top_5[0]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero3:'"+top_5[0]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass



    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero1:'"+top_5[1]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero2:'"+top_5[1]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero3:'"+top_5[1]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero1:'"+top_5[2]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero2:'"+top_5[2]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass


    try:
        query = "match (n:Database{nombre:'"+nombre+"'})-[:contains*1..3]->(a:Database{genero3:'"+top_5[2]+"'}) return collect(distinct a.nombre)"
        #query = "MATCH (n:Database {genero1:'"+top_5[0]+"', genero2:'"+top_5[1]+"', genero3:'"+top_5[2]+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        #print results
        a = results.rows
        #print len(a[0][0])
        b = []
        print a[0][0][0]
        for x in a[0][0]:
            if x not in b:
                b.append(x)



        valor = random.sample(range(0, len(b)+1), 3)

        print b[valor[0]]
        print b[valor[1]]
        print b[valor[2]]

    except Exception:
        pass

    #YourList.OrderBy(x => rnd.Next()).Take(5)
    #recomendation(name, top_5[0], top_5[1], top_5[2], top_5[3])


#mÃ©todo para mostrar todas las series y peliculas de un genero
def show_genre():
    genre = raw_input("Insert genre: ")
    try:
        query = "MATCH (n:Database {genero1:'"+genre+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        a = results.rows
        b = []
        for x in a:
            if x not in b:
                b.append(x)
                print x

    except Exception:
        pass

    try:
        query = "MATCH (n:Database {genero2:'"+genre+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        a = results.rows
        b = []
        for x in a:
            if x not in b:
                b.append(x)
                print x

    except Exception:
        pass

    try:
        query = "MATCH (n:Database {genero3:'"+genre+"'}) RETURN n.nombre"
        results = db.query(query, data_contents=True)
        a = results.rows
        b = []
        for x in a:
            if x not in b:
                b.append(x)
                print x

    except Exception:
        pass



#******************************************************************************************************
#*******************************************************************************************************



def menu():
    print("0. Add movies and TV shows to from Excel to Database")
    print("1. Add move or TV show to Database")
    print("2. Watch movie or TV Show")
    print("3. List of movies and TV shows by genre")
    print("9. Exit")


menu()
opcion = input("Option: ")
print ("**********************************")
print ("**********************************")

while(opcion != 9):
    if(opcion == 0):
        add_Excel()
        print ("**********************************")
        print ("**********************************")
        print ("Values added to Database")
        menu()
        opcion = input("Option: ")

    elif(opcion == 1):
        add_database()
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Option: ")

    elif(opcion == 2):
        watch()
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Option: ")

    elif(opcion == 3):
        show_genre()
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Option: ")

    else:
        print("This option is not valid")
        print ("**********************************")
        print ("**********************************")
        menu()
        opcion = input("Option: ")

print ("Thanks for using the program")
