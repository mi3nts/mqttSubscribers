
from getmac import get_mac_address
import serial.tools.list_ports
import yaml


# Change Accordingly  
mintsDefinitions = yaml.load(open('mintsXU4/mintsDefinitions.yaml'),Loader=yaml.FullLoader)
dataFolder       = mintsDefinitions['dataFolder']
dataFolderReference       = mintsDefinitions['dataFolder'] + "/reference"
dataFolderMQTTReference   = mintsDefinitions['dataFolder'] + "/referenceMqtt"  # The path of your MQTT Reference Data 
dataFolderMQTT            = mintsDefinitions['dataFolder'] + "/rawMqtt"        # The path of your MQTT Raw Data 
tlsCert                   = "/mfs/io/groups/lary/certs/ca-certificates.crt"     # The path of your TLS cert


#  -------------------------- 

latestOn                  = False

# For MQTT 
mqttOn                    = True
mqttCredentialsFile       = 'mintsXU4/credentials.yml'
mqttLoRaCredentialsFile   = 'mintsXU4/loRacredentials.yml'


sensorNodesFile          = 'sensorNodes.yml'
droneFile                = 'drone.yml'
centralNodesFile         = 'centralNodes.yml'
loRaNodesFile            = 'loRaNodes.yml'
otterFile                = 'otter.yml'
carRoofFile              = 'carRoof.yml'
utdNodesFile             = 'utdNodes.yml'
mockNodesFile            = 'sensorNodesMock.yml'
mqttBroker               = "mqtt.circ.utdallas.edu"
mqttBrokerLoRa           = "mqtt.lora.trecis.cloud"
mqttPort                 = 8883  # Secure port
mqttPortLoRa             = 1883  # Secure port
senderNodes              = yaml.load(open(sensorNodesFile),Loader=yaml.FullLoader)




def findMacAddress():
    macAddress= get_mac_address(interface="eth0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="docker0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp1s0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    return "xxxxxxxx"

macAddress                = findMacAddress()

print()
print("----MINTS Definitions-----")
print("Mac Address                : {0}".format(macAddress))
print("Latest On                  : {0}".format(latestOn))
print("MQTT On                    : {0}".format(mqttOn))
print("MQTT Credentials File      : {0}".format(mqttCredentialsFile))
print("MQTT Broker and Port       : {0}, {1}".format(mqttOn,mqttPort))
print("Sensor Nodes File          : {0}".format(sensorNodesFile))

#dataFolder                = "/home/teamlary/mintsData/raw"
#dataFolderReference       = "/home/teamlary/mintsData/reference"
