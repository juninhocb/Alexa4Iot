import paho.mqtt.client as mqtt
from components.client import *

listObjects = []

### Funções primárias
###################################################################################################################### 

def connect (handler_input):
    speakOut = ""
    device = catchDevice (handler_input) 
    if isConnect(device):
        speakOut = "Dispositivo " + device + " já está conectado!"
    else: 
        obj = Client ('', device)
        if obj.onConnect():  
            listObjects.append(obj) 
            speakOut = "Dispositivo " + device + " conectado com sucesso! " 
        else: 
            speakOut = "Houve uma falha ao tentar conectar-se ao Broker"
    
    return speakOut

def listConnected ():
    speakOut = ""
    aux = ""
    if listObjects != []:
        for i in listObjects:
            aux = aux + ". " + i.getDevice() 
                
        speakOut = "Dispositivos conectados: " + aux
    else:
        speakOut = "Não há dispositivos conectados"
    
    return speakOut

def disconnect(handler_input):
    speakOut = ""
    device = catchDevice(handler_input)
    if isConnect(device):
        obj = catchSelected(device)
        index = catchIndex(device)
        obj.on_disconnect = on_disconnect
        msgOut = "Adeus dispositivo " + obj._client_id.decode()
        obj.publish("Monitoring", msgOut)
        listObjects.pop(index)
        obj.disconnect()
        speakOut = "Dispositivo " + obj._client_id.decode() + " desconectado com sucesso!"
    else:
        speakOut = "Dispositivo " + device + " já está desconectado!"
    
    return speakOut

def feed(handler_input):
    msgOut = ""
    topicOut = ""
    speakOut = ""
    device = catchDevice(handler_input)
    portions = catchQuantity(handler_input)
    if isConnect(device):
        obj = catchSelected(device)
        msgOut = "1"+ portions
        topicOut = obj._client_id.decode()
        print(msgOut)
        print(topicOut)
        obj.publish(topicOut, msgOut)
        speakOut = "O <sua requisição> " + device + "irá <ação> em " + portions + " <quantidade>."
        
    else:
        speakOut = "O dispositivo " + device + "está desconectado, favor conectar para <sua ação>!"
    
    return speakOut

####################################################################################################################### 
# Funções auxiliares

def catchDevice(handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    return slots['device'].resolutions.resolutions_per_authority[0].values[0].value.name

def catchQuantity(handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    return slots['quantity'].value

def isConnect(device):
    for i in listObjects:
        if i.getDevice() == device:
            return True
    
    return False

def catchSelected(device):
    for i in listObjects:
        if i.getDevice() == device:
            return i.getObjMQTT()

def catchIndex(device):
    count = 0
    for i in listObjects:
        if i.getDevice() == device:
            return count
        else: 
            count = count + 1
        
    return count 

def on_disconnect(client, userdata, rc):
    print("desconectado com sucesso %s", rc)
            
            
            
            
            
            
            
            