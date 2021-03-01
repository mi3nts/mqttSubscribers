# mqttSubscribers
Contains codes which subscribes into MINTS mqtt data streams

## Instructions 
- Gaining the credentials file.
  Please contact a team member at mints to download the credentials.yml file. Once received place the file `mintsXU4` folder. 
    - ```mqttSubscribers/firmware/mintsXU4/credentials.yml```
 -  Change lines 8 - 10 on ```mqttSubscribers/firmware/mintsXU4/mintsDefinitions.py``` to match your preference. Here you are choosing where you would store the csv files from the data generated with the MQTT stream on your local machine as well as the location of your tls Certificate.
 ```
dataFolderMQTTReference   = "/home/teamlary/mintsData/referenceMQTT"  # The path of your MQTT Reference Data 
dataFolderMQTT            = "/home/teamlary/mintsData/rawMQTT"        # The path of your MQTT Raw Data 
tlsCert                   = "/etc/ssl/certs/ca-certificates.crt"     # The path of your TLS cert
```
 - Run the approprate subscriber code on your terminal.
    - Eg: ```./mintsGroundVehicle.sh```
    
  
 
 
