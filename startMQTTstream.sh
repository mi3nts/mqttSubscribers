#!/bin/bash


source env/bin/activate
cd firmware
python groundVehicleDataRead.py & 
sleep 10 
python otterDataRead.py
sleep 10 
python centralNodesDataRead.py
