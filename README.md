# Rika-Firenet
Code Python pour controller un poêle RIKA au travers d'un FIRENET
A python based script for monitoring, analytics and control for Home-Assistant.

This project is based on code from [IERO](https://github.com/iero/Rika-Stove).

## Dependancies (with tested version)
* $ pip install colorama==0.3.7
* $ pip install requests==2.18.4
* $ pip install beautifulsoup4==4.8.1
* $ pip install paho_mqtt==1.4.0
* A functionnal MQTT server...

## Features

* Access the RIKA-FIRENET web interface to retrieve information.
* Use MQTT to publish the information

## Preview

Information :
               Starting Rika Update (13.11.19 02:11)
               Connecting to Firenet...
               Connected to Rika !
Global :
               Stove                  : Salon [xyxyxyxyxy]
               Last seen              : 0 min ago
               Last Revision          : 13/11/2019 02:10
Control :
               Last Revision          : 13/11/2019 02:10
               Stove                  : is online
               Operating mode         : Comfort with 60% power
               Target Temperature     : 21 degC
               Protection Temperature : 16 degC
Sensors :
               Stove                  : Standby
               Room Temperature       : 20 degC
               Flame Temperature      : 17 degC
               Pellets consumption    : 941 Kg (721 h)
               Pellets nbre de sacs   : 62.73 sacs
               Diag Motor             : 0 %
               Fan velocity           : 0 rps
MQTT :
               Connecting to broker   : xxx.xxx.xxx.xxx
                                      : Connected!
               Sending MQTT data      : Please wait...
                                      : MQTT Sent

## Installation and Support

* Install python dependencies according requirements.txt
* Edit rika_config.yaml with your information
* Run using "/usr/bin/python3 rika_domo.py" and check results

## Issues & Feature Requests

* Please see the [Issues Repository](https://github.com/MoBOatGVA/Rika-Firenet/issues).

## License

This is free software under the GPL v3 open source license. Feel free to do with it what you wish, but any modification must be open sourced. A copy of the license is included.
