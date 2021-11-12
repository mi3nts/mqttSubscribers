# ***************************************************************************
#  mintsXU4
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: February 4th, 2019
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************

import serial
import datetime
import os
import csv
import deepdish as dd
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsSensorReader as mSR
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import netifaces as ni
import math
import base64
import json
import struct

macAddress     = mD.macAddress
dataFolder     = mD.dataFolder
dataFolderMQTT = mD.dataFolderMQTT
dataFolderMQTTReference = mD.dataFolderMQTTReference
latestOn       = mD.latestOn
mqttOn         = mD.mqttOn
decoder        = json.JSONDecoder(object_pairs_hook=OrderedDict)

def sensorSendLoRa(dateTime,gatewayID,nodeID,sensorID,framePort,base16Data):
    if(sensorID=="IPS7100"):
        IPS7100LoRaWrite(dateTime,gatewayID,nodeID,sensorID,framePort,base16Data)

def IPS7100LoRaWrite(dateTime,gatewayID,nodeID,sensorID,framePort,base16Data):
    if(framePort == 15):
        sensorDictionary =  OrderedDict([
                ("dateTime" , str(dateTime)), 
        		("pc0_1"  ,struct.unpack('<L',bytes.fromhex(base16Data[0:8]))[0]),
            	("pc0_3"  ,struct.unpack('<L',bytes.fromhex(base16Data[8:16]))[0]),
                ("pc0_5"  ,struct.unpack('<L',bytes.fromhex(base16Data[16:24]))[0]),
                ("pc1_0"  ,struct.unpack('<L',bytes.fromhex(base16Data[24:32]))[0]),
            	("pc2_5"  ,struct.unpack('<L',bytes.fromhex(base16Data[32:40]))[0]),
        		("pc5_0"  ,struct.unpack('<L',bytes.fromhex(base16Data[40:48]))[0]), 
            	("pc10_0" ,struct.unpack('<L',bytes.fromhex(base16Data[48:56]))[0]),
        		("pm0_1"  ,struct.unpack('<f',bytes.fromhex(base16Data[56:64]))[0]), 
            	("pm0_3"  ,struct.unpack('<f',bytes.fromhex(base16Data[64:72]))[0]),
                ("pm0_5"  ,struct.unpack('<f',bytes.fromhex(base16Data[72:80]))[0]),
                ("pm1_0"  ,struct.unpack('<f',bytes.fromhex(base16Data[80:88]))[0]),
            	("pm2_5"  ,struct.unpack('<f',bytes.fromhex(base16Data[88:96]))[0]),
        		("pm5_0"  ,struct.unpack('<f',bytes.fromhex(base16Data[96:104]))[0]), 
            	("pm10_0" ,struct.unpack('<f',bytes.fromhex(base16Data[104:112]))[0])
        ])
    print(sensorDictionary)        
    loRaWriteFinisher(nodeID,sensorID,dateTime,sensorDictionary)
    return ;

def loRaWriteFinisher(nodeID,sensorID,dateTime,sensorDictionary):
    writePath = mSR.getWritePathMQTT(nodeID,sensorID,dateTime)
    exists    = mSR.directoryCheck(writePath)
    # print("Writing MQTT Data")
    # print(writePath)
    mSR.writeCSV2(writePath,sensorDictionary,exists)
    mL.writeJSONLatestMQTT(sensorDictionary,nodeID,sensorID)
    return;



def loRaSummaryWrite(message,portIDs):
    nodeID = message.topic.split('/')[5]
    sensorPackage       =  decoder.decode(message.payload.decode("utf-8","ignore"))
    rxInfo              =  sensorPackage['rxInfo'][0]
    txInfo              =  sensorPackage['txInfo']
    loRaModulationInfo  =  txInfo['loRaModulationInfo']
    sensorID            = portIDs[getPortIndex(sensorPackage['fPort'],portIDs)]['sensor']
    dateTime            = datetime.datetime.fromisoformat(sensorPackage['publishedAt'][0:26])
    base16Data          = base64.b64decode(sensorPackage['data'].encode()).hex()
    gatewayID           = base64.b64decode(rxInfo['gatewayID']).hex()
    framePort           = sensorPackage['fPort']
    sensorDictionary =  OrderedDict([
            ("dateTime"        , str(dateTime)),
            ("gatewayID"       , gatewayID ),
            ("rssi"            , rxInfo["rssi"]),
            ("loRaSNR"         , rxInfo["loRaSNR"]),
            ("channel"         , rxInfo["channel"] ),
            ("rfChain"         , rxInfo["rfChain"] ),
            ("frequency"       , txInfo["frequency"]),
            ("bandwidth"       , loRaModulationInfo["bandwidth"]),
            ("spreadingFactor" , loRaModulationInfo["spreadingFactor"] ),
            ("codeRate"        , loRaModulationInfo["codeRate"] ),
            ("dataRate"        , sensorPackage['dr']),
            ("frameCounters"   , sensorPackage['fCnt']),
            ("framePort"       , framePort),
            ("base64Data"      , sensorPackage['data']),
            ("base16Data"      , base16Data),
            ("devAddr"         , sensorPackage['devAddr']),
            ("sensorID"        , sensorID  ),
            ("deviceAddDecoded", base64.b64decode(sensorPackage['devAddr'].encode()).hex())
        ])

    loRaWriteFinisher("LoRaNodes","Summary",dateTime,sensorDictionary)
    loRaWriteFinisher(gatewayID,"Summary",dateTime,sensorDictionary)
    return dateTime,gatewayID,nodeID,sensorID,framePort,base16Data;

def getPortIndex(portIDIn,portIDs):
    indexOut = 0
    for portID in portIDs:
        if (portIDIn == portID['portID']):
            return indexOut; 
        indexOut = indexOut +1
    return -1;
