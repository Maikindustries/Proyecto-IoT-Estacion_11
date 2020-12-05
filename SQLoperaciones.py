import os
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import yagmail


def hacerInstruccion(opcion,idPaciente,dato):
    #conexion a base de datos
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="estacion_11"
    )
    mycursor=mydb.cursor()
    """
    1) Agregar telefono
    2) Agregar sintoma
    3) Agregar medicamento
    4) Agregar enfermedad
    """

    if opcion==1:
        mycursor.execute(f"INSERT INTO `telefonos` (`idTelefono`, `idPaciente`, `telefono`) VALUES (NULL, '{idPaciente}', '{dato}')")
    elif opcion==2:
        mycursor.execute(f"INSERT INTO `sintomas` (`idSintoma`, `idPaciente`, `sintoma`) VALUES (NULL, '{idPaciente}', '{dato}')")
    elif opcion==3:
        mycursor.execute(f"INSERT INTO `medicamentos` (`idMedicamento`, `idPaciente`, `medicamento`) VALUES (NULL, '{idPaciente}', '{dato}')")
    else:
        mycursor.execute(f"INSERT INTO `antecedentes` (`idAntecedente`, `idPaciente`, `antecedente`) VALUES (NULL, '{idPaciente}', '{dato}')")
    mydb.commit()
    mycursor.close()
    
#grabarDatos 
def agregarPersona():
    n="n"
    N="N"
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="estacion_11"
    )
    
    mycursor=mydb.cursor()
    print("Ingrese los siguientes datos")
    nombres=input("Nombres\n").capitalize()
    apellidoP=input("ApellidoPaterno\n").capitalize()
    apellidoM=input("ApellidoMaterno\n").capitalize()
    fechaNac=input("Ingrese su fecha de nacimiento en el siguiente formato YYYY-MM-DD:\n")
    sexoP=input("Ingrese su sexo en el siguiente formato:\nMasculino: M  Femenino: F\n").upper()
    ciudadP=input("Ingrese su ciudad\n").upper()
    delegacionP=input("Ingrese su delegacion\n").capitalize()
    direccionP=input("Ingrese su dirección\n").capitalize()
    correoP=input("Ingrese su correo\n")
    
    #Query agregar usuario
    mycursor.execute(f"INSERT INTO `paciente` (`idPaciente`, `nombres`, `apellidoPaterno`, `apellidoMaterno`, `fechaNacimiento`, `sexo`, `ciudad`, `delegacion`, `direccion`, `correo`) VALUES (NULL, '{nombres}', '{apellidoP}', '{apellidoM}', '{fechaNac}', '{sexoP}', '{ciudadP}', '{delegacionP}', '{direccionP}', '{correoP}')")
    mydb.commit()
    #query obtener iD
    mycursor.execute("SELECT MAX(paciente.idPaciente) FROM paciente")
    
    for i in mycursor:
        idPaciente=i[0]
        print(f"Su id de paciente es {i[0]}")
    
    #Tablas aparte
    telefono=input("Ingrese su telefono\n")
    resp=telefono
    if resp!=n:
        hacerInstruccion(1,idPaciente,resp)
        estado=True
        while(estado):
            resp=input("Si desea ingresar otro telefono, digite el numero.\nSi no desea ingresar otro telefono, digite N\n")
            if resp==n or resp==N:
                estado=False
            else:
                hacerInstruccion(1,idPaciente,resp)
            
    sintomaP=input("Ingrese su sintoma\n")
    resp=sintomaP
    if resp!=n:
        hacerInstruccion(2,idPaciente,resp)
        estado=True
        while(estado):
            resp=input("Si desea ingresar otro sintoma, ingrese el sintoma.\nSi no desea ingresar otro sintoma, digite N\n")
            if resp==n or resp==N:
                estado=False
            else:
                hacerInstruccion(2,idPaciente,resp)
        
        
    medicamentoP=input("En caso de estar tomando medicamentos\ningrese el nombre uno por uno. De lo contrario ingrese  N\n")
    resp=medicamentoP
    if resp!=n:
        hacerInstruccion(3,idPaciente,resp)
        estado=True
        while(estado):
            resp=input("Ingrese otro medicamento\nSi ya no desea ingresar otro medicamento ingrese  N\n")
            if resp==n or resp==N:
                estado=False
            else:
                hacerInstruccion(3,idPaciente,resp)
    
    
    enfermedadP=input("En caso de padecer enfermedades, ingrese una por una\nDe lo contrario, ingrese  N\n")
    resp=enfermedadP
    if resp!=n:
        hacerInstruccion(4,idPaciente,resp)
        estado=True
        while(estado):
            resp=input("Ingrese otra enfermedad\nSi ya no desea ingresar otra enfermedad ingrese  N\n")
            if resp==n or resp==N:
                estado=False
            else:
                hacerInstruccion(4,idPaciente,resp)
    
    mycursor.close()

def consulta():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="estacion_11"
    )
    
    estado=True
    while(estado):
        mycursor=mydb.cursor()
        consul = int(input('¿Qué gráfica desea ver?\n1.Ciudades\n2.Sexo de los pacientes\n3.Cantidad de personas con ciertos síntomas\n4.Temperatura corporal\n5.Ritmo Cardiáco\n6.Humedad Habitación\n7.Temperatura Habitación\n8.Enviar correo a paciente\n9.Registrarse en la base de datos\n'))
        if (consul==1):
            mycursor.execute("SELECT DISTINCT ciudad,COUNT(ciudad) FROM `paciente` GROUP BY ciudad")
            titulo="Ciudades"
            paraPay(mycursor,titulo)
        elif(consul==2):
            titulo="Sexo"
            mycursor.execute("SELECT DISTINCT sexo,COUNT(sexo) FROM `paciente` GROUP BY sexo")
            paraPay(mycursor,titulo)
        elif(consul==3):
            titulo="Síntomas"
            mycursor.execute("SELECT DISTINCT sintoma,COUNT(sintoma) FROM `sintomas` GROUP BY sintoma")
            paraPay(mycursor,titulo)
        elif(consul==4):
            titulo="Temperatura corporal"
            idPaciente=input('¿Cuál es la id del paciente que requiere graficar la información?\n')
            try:
                mycursor.execute("SELECT idPaciente FROM `paciente` WHERE idPaciente={0}".format(idPaciente))
                for x in mycursor:
                    idPac=x
                mycursor.execute("SELECT medicion FROM `temperaturapaciente` WHERE idPaciente={0}".format(idPaciente))
                paraGrafica(idPaciente, mycursor,titulo)
            except:
                print("Error: No existe el usuario ingresado")

        elif(consul==5):
            titulo="Ritmo Cardiáco"
            idPaciente=input('¿Cuál es la id del paciente que requiere graficar la información?\n')
            try:
                mycursor.execute("SELECT idPaciente FROM `paciente` WHERE idPaciente={0}".format(idPaciente))
                for x in mycursor:
                    idPac=x
                mycursor.execute("SELECT  medicion FROM ritmocardiaco WHERE idPaciente={0}".format(idPaciente))
                paraGrafica(idPaciente, mycursor,titulo)
            except:
                print("Error: No existe el usuario ingresado")

            
        elif(consul==6):
            titulo="Humedad Habitación"
            idPaciente=input('¿Cuál es la id del paciente que requiere graficar la información?\n')
            try:
                mycursor.execute("SELECT idPaciente FROM `paciente` WHERE idPaciente={0}".format(idPaciente))
                for x in mycursor:
                    idPac=x
                mycursor.execute("SELECT medicionHumedad FROM humedadhabitacion WHERE idPaciente={0}".format(idPaciente))
                paraGrafica(idPaciente, mycursor,titulo)
            except:
                print("Error: No existe el usuario ingresado")

        elif(consul==7):
            titulo="Temperatura Habitación"
            idPaciente=input('¿Cuál es la id del paciente que requiere graficar la información?\n')
            try:
                mycursor.execute("SELECT idPaciente FROM `paciente` WHERE idPaciente={0}".format(idPaciente))
                for x in mycursor:
                    idPac=x
                mycursor.execute("SELECT medicionTemperatura FROM humedadhabitacion WHERE idPaciente={0}".format(idPaciente))
                paraGrafica(idPaciente, mycursor,titulo)
            except:
                print("Error: No existe el usuario ingresado")
            
        elif(consul==8):
            idPaciente=input('¿Cuál es la id del paciente al que desea contactar?\n')
            try:
                mycursor.execute("SELECT idPaciente FROM `paciente` WHERE idPaciente={0}".format(idPaciente))
                for x in mycursor:
                    idPac=x[0]
                    
                mycursor.execute("SELECT correo FROM `paciente` WHERE idPaciente={0}".format(idPaciente))                
                for x in mycursor:
                    correoPaciente=x[0]
                enviarCorreo(correoPaciente)
            except:
                print("Error: Usuario no registrado o correo inválido.")
        elif(consul==9):
            agregarPersona()
        else:
            print('Ingrese una opción válida')
            consulta()
            
        resp=input('¿Desea hacer otra consulta? (S/N) \n')
        if (resp.upper()!='S'):
            estado=False
        
        
def paraPay(mycursor,titulo):
    lista=[]
    for x in mycursor:
        lista.append(x)
    mycursor.close()
    
    lista1=[]
    lista2=[]
    for i in lista:
        lista1.append(i[0])
        lista2.append(i[1])
    graficaPie(lista1,lista2,titulo)
    
def paraGrafica(idPaciente, mycursor,titulo):
    lista=[]
    for x in mycursor:
        lista.append(x)
    mycursor.close()
    
    lista1=[]
    for i in lista:
        lista1.append(i[0])
    graficarDatos(idPaciente,lista1,titulo)

def graficaPie(listaLabel,listaDatos,titulo):
    lista=listaLabel
    listaNumeros=listaDatos
    
    normdata = colors.Normalize(min(listaNumeros), max(listaNumeros))
    colormap = cm.get_cmap("Blues")
    colores =colormap(normdata(listaNumeros))

    plt.pie(listaNumeros, labels=lista, autopct="%0.1f %%", colors =colores)
    plt.axis("equal")
    plt.title(titulo)
    plt.show()
    
def graficarDatos(idPaciente, lista,titulo):
    y=lista
    x=[]
    for i in range(0,len(y)):
        x.append(i)
    if len(y)!=0:
        plt.axis([0,max(x),min(y)-1,max(y)+1])
        plt.plot(x,y)
        plt.xlabel('# de medición')
        plt.ylabel('Medición')
        plt.title('{0} ID Paciente {1}'.format(titulo,idPaciente))
        plt.show()
    else:
        print("No hay datos para graficar")

def enviarCorreo(correoPaciente):
    correoDoctor=input("Ingrese su correo electrónico\n")
    contraDoctor=input("Ingrese su contraseña\n")
    correo=yagmail.SMTP(correoDoctor,contraDoctor)
    mensaje=input("Escriba el mensaje que desea enviar al paciente\n")
    correo.send(to=f"{correoPaciente}",subject="Respuesta Doctor",contents=mensaje)

def main():
    consulta()
    
main()
