import paho.mqtt.client as mqttCli
from paho import mqtt

class Client ():
    def __init__(self, objMQTT, device):
        self.__objMQTT = objMQTT # Objeto MQTT
        self.__device = device  # nome do dispositivo passado pelo usuário: ex: pote um


    def onConnect(self):
        try:
            welcomePublish = ""
            self.client = mqttCli.Client(self.__device)
            self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
            self.client.username_pw_set("<your_username>", "<your_password>")
            self.__objMQTT = self.client
            self.client.connect("<your_public_broker>", <"port">)
            welcomePublish = "Dispositivo " + self.__device + "conectado com sucesso!" 
            self.client.publish("Monitoring", welcomePublish)
            self.client.loop_start()
            return True
        except:
            return False
    
    def getObjMQTT (self):
        
        return self.__objMQTT
    
    def getDevice (self):
        
        return self.__device
    
        
    
    