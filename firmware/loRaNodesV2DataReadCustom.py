# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
import base64
from pickle import TRUE
import paho.mqtt.client as mqtt
import datetime
import yaml
import collections
import json

from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsLoRaReader as mLR
from collections import OrderedDict
import struct

mqttPort            = mD.mqttPortLoRa
mqttBroker          = mD.mqttBrokerLoRa
mqttCredentialsFile = mD.mqttLoRaCredentialsFile
fileIn              = mD.loRaNodesFile
customLoRaNodesFile = mD.customLoRaNodesFile
tlsCert             = mD.tlsCert

# credentials     = yaml.load(open(mqttCredentialsFile),Loader=yaml.FullLoader)
transmitDetail   = yaml.load(open(fileIn),Loader=yaml.FullLoader)
customLoraNodes  = yaml.load(open(customLoRaNodesFile),Loader=yaml.FullLoader)

print("Custom Lora Nodes:")
print(customLoraNodes['nodes'])


tlsCert             = mD.tlsCert
portIDs             = transmitDetail['portIDs']

credentials  = yaml.load(open(mqttCredentialsFile),Loader=yaml.FullLoader)
connected    = False  # Stores the connection status
broker       = mqttBroker  
port         = mqttPort  # Secure port
mqttUN       = credentials['mqtt']['username'] 
mqttPW       = credentials['mqtt']['password'] 

decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    topic = "utd/lora/app/2/device/+/event/up"
    client.subscribe(topic)
    print("Subscrbing to Topic: "+ topic)

def on_message(client, userdata, msg):
    try:
        # print()
        # print(" - - - MINTS DATA RECEIVED - - - ")
        # print(msg.payload)
        dateTime,gatewayID,nodeID,sensorID,framePort,base16Data = \
            mLR.loRaSummaryWriteRO(msg,portIDs)
        

        if nodeID in customLoraNodes['nodes']:
       
            print()
            print(" - - - MINTS DATA RECEIVED - - - ")
            print("Node ID         : " + nodeID)
            print("Gateway ID      : " + gatewayID)
            print("Sensor ID       : " + sensorID)
            print("Date Time       : " + str(dateTime))
            print("Port ID         : " + str(framePort))
            print("Base 16 Data    : " + base16Data)
            mLR.sensorSendLoRa(dateTime,nodeID,sensorID,framePort,base16Data)
        
    
    except Exception as e:
        print("[ERROR] Could not publish data, error: {}".format(e))


# # Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqttUN,mqttPW)
client.connect(broker, port, 60)
client.loop_forever()

