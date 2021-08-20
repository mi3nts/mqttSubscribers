#!/bin/bash


source env/bin/activate
cd firmware
python groundVehicleDataRead.py & 
sleep 5 
python otterDataRead.py
sleep 5 
python centralNodesDataRead.py
