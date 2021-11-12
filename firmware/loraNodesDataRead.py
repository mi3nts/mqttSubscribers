# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
import base64
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
tlsCert             = mD.tlsCert

# credentials     = yaml.load(open(mqttCredentialsFile),Loader=yaml.FullLoader)
transmitDetail  = yaml.load(open(fileIn),Loader=yaml.FullLoader)

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
    print()
    print(" - - - MINTS DATA RECEIVED - - - ")
    dateTime,gatewayID,nodeID,sensorID,framePort,base16Data = mLR.loRaSummaryWrite(msg,portIDs)
    print("Node ID         : " + nodeID)
    print("Gateway ID      : " + gatewayID)
    print("Sensor ID       : " + sensorID)
    print("dateTime        : " + str(dateTime))
    print("Base 16 Data    : " + base16Data)
    mLR.sensorSendLoRa(dateTime,gatewayID,nodeID,sensorID,framePort,base16Data)
   

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqttUN,mqttPW)
client.connect(broker, port, 60)
client.loop_forever()