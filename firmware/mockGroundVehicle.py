# Read CSV 
# Report Time in GMT 
# import pandas as pd
import time 
import site
import sys
sys.path.append("c:\\users\\lakit\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\")
import csv
from collections import OrderedDict
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsSensorReader as mSR
import datetime

def mqttMocker(fileName,sensorName,delayIn):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            if(sensorName=="FRG001"):
                row["dateTime"]  = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            else:
                row["dateTime"]  = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(row)
            mL.writeMQTTLatestMock(row,sensorName)
            time.sleep(delayIn)
  
            

if __name__ == "__main__":
    while(True):    
        mqttMocker(sys.argv[1],sys.argv[2],float(sys.argv[3]))
    
  