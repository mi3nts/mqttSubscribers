# mqttSubscribers
Contains codes which subscribes into MINTS mqtt data streams

## Instructions 
- Gaining the credentials file.
  Please contact a team member at mints to download the credentials.yml file. Once received place the file `mintsXU4` folder. 
    - ```mqttSubscribers/firmware/mintsXU4/credentials.yml```
 -  Change lines 23 - 24 on ```mqttSubscribers/firmware/mintsXU4/mintsDefinitions.py``` to match your preference. Here you are choosing where you would store the csv files from the data generated with the MQTT stream on your local machine. 
 - Run the approprate subscriber code on your terminal.
    - Eg: ```python3 mintsGroundVehicle.py```
    
  
 
 
