# Rika-Firenet
Python script to retrieve information from a RIKA DOMO using the FIRENET option (web based).
The script should work with other models with minor changes.

This version is made to monitoring, analytics and control for Home-Assistant using a MQTT solution.

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

![Script display](https://github.com/MoBOatGVA/Rika-Firenet/blob/master/rika_domo_display.png)

## Installation and Support

* Install python dependencies according requirements.txt
* Edit rika_config.yaml with your information
* Run using "/usr/bin/python3 rika_domo.py" and check results

## Issues & Feature Requests

* Please see the [Issues Repository](https://github.com/MoBOatGVA/Rika-Firenet/issues).

## License

This is free software under the GPL v3 open source license. Feel free to do with it what you wish, but any modification must be open sourced. A copy of the license is included.
