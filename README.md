# Rika-Firenet
Python script to retrieve information from a RIKA DOMO using the FIRENET option (web based).
The script should work with other models with minor changes.

This version is made to monitoring, analytics and control for Home-Assistant using a MQTT solution.

This project is based on code from [IERO](https://github.com/iero/Rika-Stove).

## Dependencies (with tested version)
* $ pip install colorama==0.3.7
* $ pip install requests==2.18.4
* $ pip install beautifulsoup4==4.8.1
* $ pip install paho_mqtt==1.4.0
* A functionnal MQTT server...

## Features

* Access the RIKA-FIRENET web interface to retrieve information.
* Use MQTT to publish the information

## Preview

![Script display](https://github.com/MoBOatGVA/Rika-Firenet/blob/master/rika_domo_display.png)

## Installation and Support

* Install python dependencies according requirements.txt
* Edit rika_config.yaml with your information
* Run using "/usr/bin/python3 rika_domo.py" and check results
* Make sure MQTT is configured on your configuration.yaml file in Home Assitant
```
# configuration.yaml
# MQTT Broker (internal)
mqtt:
  broker: !secret mosquittoip
  username: !secret mosquittouser
  password: !secret mosquittopass
```
* Add sensors in Home-Assistant (change topic according your rika_config.yaml
```
#########################################################################
#                                 RIKA                                  #
#########################################################################
sensors:
- platform: mqtt
  name: "Rika Check Time"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["check_time"] }}'
- platform: mqtt
  name: "Rika Room Temp"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["room_temp"] }}'
  unit_of_measurement: "°C"
- platform: mqtt
  name: "Rika Pellets Used"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["pellets_used"] }}'
  unit_of_measurement: "Kg"
- platform: mqtt
  name: "Rika Pellets Time"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["pellets_time"] }}'
  unit_of_measurement: hours
- platform: mqtt
  name: "Rika Status"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["stove_status"] }}'
- platform: mqtt
  name: "Rika Flame Temperature"
  force_update: True
  state_topic: "tele/rika/SENSOR"
  value_template: '{{ value_json["SENSOR"]["flame_temp"] }}'
  unit_of_measurement: "°C"
```
* More information can be created with if needed from rika_domo.py, line 159 (json_data=...)

## Issues & Feature Requests

* Please see the [Issues Repository](https://github.com/MoBOatGVA/Rika-Firenet/issues).

## License

This is free software under the GPL v3 open source license. Feel free to do with it what you wish, but any modification must be open sourced. A copy of the license is included.
