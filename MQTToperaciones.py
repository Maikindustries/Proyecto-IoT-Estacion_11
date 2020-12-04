import time
import paho.mqtt.client as mqttClient
import matplotlib.pyplot as plt


def crearArchivoDatos(mensaje):
    mensajeNuev = str(mensaje)
    idPaciente=mensajeNuev[:2]
    print(mensajeNuev)
    t=open((str(idPaciente)) + "_Mediciones_Temperatura_Corporal.txt","a")
    r=open((str(idPaciente)) + "_Mediciones_Ritmo_Cardiaco.txt","a")
    h=open((str(idPaciente))+ "_Mediciones_Humedad_Habitacion.txt","a")
    th=open((str(idPaciente)) + "_Mediciones_Temperatura_Habitacion.txt","a")
    n=open((str(idPaciente))+ "_Mediciones_Nivel_Oxigenacion.txt","a")

    numMedicion=mensaje[5:7]
        
    tipoMedicion=str(mensaje[2:4])
        
        
    if (tipoMedicion == "TP"):
        t.write(str(numMedicion)+"\n")
        t.close()
    elif (tipoMedicion == "RC"):
        r.write(str(numMedicion)+"\n")
        r.close()
    elif (tipoMedicion == "HH"):
        h.write(str(numMedicion)+"\n")
        h.close()
    elif(tipoMedicion == "NO"):
        n.write(str(numMedicion)+"\n")
        n.close()
    elif(tipoMedicion == "TH"):
        th.write(str(numMedicion)+"\n")
        th.close()


def graficarDatos():
    idPaciente=input("Digite el id del paciente\n")
    try:
        y,medicion=leerArchivo(idPaciente)
        x=[]
        for i in range(0,len(y)):
            x.append(i)
        if len(y)!=0:
            plt.axis([0,max(x),min(y)-1,max(y)+1])
            plt.plot(x,y)
            plt.xlabel('Número de medición')
            plt.ylabel('Medición')
            plt.title('{0} ID Paciente{1}'.format(medicion,idPaciente))
            plt.show()
        else:
            print("No hay datos para graficar")
    except:
        print('')
    
    
def leerArchivo(idPaciente):
    respuesta=int(input("1.Temperatura Corporal\n2.Ritmo Cardiaco\n3.Humedad Habitacion\n4.Temperatura Habitación\n5.Nivel de Oxigenacion\n¿Qué gráfica desea ver?: "))
    try:
        t=open((str(idPaciente)) + "_Mediciones_Temperatura_Corporal.txt","r")
        r=open((str(idPaciente)) + "_Mediciones_Ritmo_Cardiaco.txt","r")
        h=open((str(idPaciente))+ "_Mediciones_Humedad_Habitacion.txt","r")
        th=open((str(idPaciente)) + "_Mediciones_Temperatura_Habitacion.txt","r")
        n=open((str(idPaciente))+ "_Mediciones_Nivel_Oxigenacion.txt","r")
        
        listT=[]
        if(respuesta==1):
            medicion="Temperatura Corporal"
            for linea in t:
                aux=linea[:2]
                listT.append(int(aux))
        elif(respuesta==2):
            medicion="Ritmo Cardíaco"
            for linea in r:
                aux=linea[:2]
                listT.append(int(aux))
        elif(respuesta==3):
            medicion="Humedad Habitación"
            for linea in h:
                aux=linea[:2]
                listT.append(int(aux))
        elif(respuesta==4):
            medicion="Temperatura Habitación"
            for linea in th:
                aux=linea[:2]
                listT.append(int(aux))
        elif(respuesta==5):
            medicion="Nivel de oxigenación"
            for linea in n:
                aux=linea[:2]
                listT.append(int(aux))
                
        print(f"La medicion es {medicion}")
        return listT,medicion
    
    except:
        print("No hay datos para graficar")
        main()
    
    
   
#definición de funciones

def on_connect(client,userdata,flags,rc):    
    if rc == 0:        
        print("Conectado al broker")        
        global Connected        
        Connected = True    
    else:        
        print("Fallo en la conexión")
def on_message(client,userdata,message):    
    print("Mensaje recibido: {}".format(message.payload))
    crearArchivoDatos(message.payload.decode("utf-8"))
    
def conectarBroker():
    Connected = False             #variable globar para verificar estado de la conexión
    broker = "broker.hivemq.com"  #ip o URL del broker
    port = 1883                   # puerto por default
    tag = "/estacion/11"   #Etiqueta
    #user = ""
    #password = ""
    clientS = mqttClient.Client("Cliente") #crea una instancia
    clientS.on_connect = on_connect        #agrega la función al objeto
    clientS.on_message = on_message
    clientS.connect(broker,port)
    clientS.loop_start()
    while Connected != True:    
        time.sleep(.1)    
        clientS.subscribe(tag)    
        try:        
            while True:            
                time.sleep(.1)    
        except KeyboardInterrupt:        
            print("Recepción de mensajes detenida por el usuario")        
            clientS.disconnect()        
            clientS.loop_stop()
    
def main():
    estado=True
    while estado:
        opcion=int(input('\nElija una opción:\n1.Recibir información del broker Hivemq\n2.Graficar datos de un paciente\n3.Cerrar programa\n'))
        if opcion==1:
            conectarBroker()
        elif opcion==2:
            graficarDatos()
        elif opcion==3:
            estado=False
        else:
            print('Elija una opción válida')
        
main()