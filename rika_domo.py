#   Version:    1.1
#   Date   :    23.02.2020
#   Source :    https://github.com/MoBOatGVA/Rika-Firenet
#

import sys
import time
import yaml
import requests
import json
import datetime
import paho.mqtt.client as mqtt
import os
from pathlib import Path
import colorama
from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings()

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup # parse page

web_response = ""

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def connect(client, url_base, url_login, url_stove, user, pwd) :
    data = {
        'email':user,
        'password':pwd}

    # retreive content of the web site in case of extended verbose
    global web_response

    r = client.post(url_base+url_login, data)
    # print(r.url)
    # print(r.text)
    web_response = r.text

    if ('logout' in r.text) == True :
        print(Fore.GREEN + '               Connected to Rika !' + Fore.RESET)

        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.find("ul", {"id": "stoveList"})
        # print(text)
        if text is not None :
            stoveName = text.find('a').text
            a = text.find('a', href=True)
            stove = a['href'].replace(url_stove,'')
            #print(Fore.GREEN + "               Found the Stove : {} [{}]".format(stoveName,stove) + Fore.RESET)
            return stove

    return ""

def set_stove_temperature(client, url_base, url_api, stove, temperature) :
    # Security : Do not set extreme values
    min = 14
    max = 24

    if min <= temperature <= max :
        cmd = '&targetTemperature='+str(temperature)
        actual = get_stove_information(client, url_base, url_api, stove)
        data = actual['controls']
        data['targetTemperature'] = str(temperature)

        r = client.post(url_base+url_api+stove+'/controls', data)

        for counter in range (0,10) :
            if ('OK' in r.text) == True :
                print('Temperature target is now {} degC'.format(temperature))
                return True
            else :
                print('In progress.. ({}/10)'.format(counter))
                time.sleep(2)
    elif temperature < min :
        print("Too cold ! {} degC minimum !".format(min))
    else :
        print("Too hot ! {} degC maximum !".format(max))

def get_stove_information(client, url_base, url_api, stove) :
    r = client.get(url_base+url_api+stove+'/status?nocache=')
    return r.json()

def show_stove_information(data) :

    print(Fore.CYAN + "Global :" + Fore.RESET)
    print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "{0} [{1}]".format(data['name'],data['stoveID']))
    print(Fore.WHITE + "               Last seen              : " + Fore.YELLOW + "{} min ago".format(data['lastSeenMinutes']))
    lastConfirmedRevision = time.strftime('%d/%m/%Y %H:%M', time.localtime(data['lastConfirmedRevision']))
    print(Fore.WHITE + "               Last Revision          : " + Fore.YELLOW + "{}".format(lastConfirmedRevision))

    print(Fore.CYAN + "Control : ")
    revision = time.strftime('%d/%m/%Y %H:%M', time.localtime(data['controls']['revision']))
    print(Fore.WHITE + "               Last Revision          : " + Fore.YELLOW + "{}".format(revision))

    if data['controls']['onOff'] :
        print(Fore.WHITE + "               Stove                  : " + Fore.GREEN + "is online")
        jstovectl = "Online"
    else :
        print(Fore.WHITE + "               Stove                  : " + Fore.RED + "is offline")
        jstovectl = "Offline"

    if data['controls']['operatingMode'] == 0 :
        print(Fore.WHITE + "               Operating mode         : " + Fore.YELLOW + "Manual with {}% power".format(data['controls']['heatingPower']))
        jstovemode = "Manual"
    elif data['controls']['operatingMode'] == 1 :
        print(Fore.WHITE + "               Operating mode         : " + Fore.YELLOW + "Automatic with {}% power".format(data['controls']['heatingPower']))
        jstovemode = "Automatic"
    elif data['controls']['operatingMode'] == 2 :
        print(Fore.WHITE + "               Operating mode         : " + Fore.YELLOW + "Comfort with {}% power".format(data['controls']['heatingPower']))
        jstovemode = "Comfort"

    print(Fore.WHITE + "               Target Temperature     : " + Fore.YELLOW + "{} degC".format(data['controls']['targetTemperature']))
    print(Fore.WHITE + "               Protection Temperature : " + Fore.YELLOW + "{} degC".format(data['controls']['setBackTemperature']))

    print(Fore.CYAN + "Sensors : ")
    if data['sensors']['statusMainState'] == 1 :
        if data['sensors']['statusSubState'] == 0 :
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "OFF")
            jstove = "Off"
        elif data['sensors']['statusSubState'] == 1 or data['sensors']['statusSubState'] == 3:
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Standby")
            jstove = "Standby"
        elif data['sensors']['statusSubState'] == 2 :
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "External command")
            jstove = "External Command"
        else :
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Unknown State")
            jstove = "UnKnown State"
    elif data['sensors']['statusMainState'] == 2 :
        print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Waking up")
        jstove = "Waking Up"
    elif data['sensors']['statusMainState'] == 3 :
        print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Starting")
        jstove = "Starting"
    elif data['sensors']['statusMainState'] == 4 :
        print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Burning (control mode)")
        jstove = "Burning (control mode)"
    elif data['sensors']['statusMainState'] == 5 :
        if data['sensors']['statusSubState'] == 3 or data['sensors']['statusSubState'] == 4 :
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Deep Cleaning")
            jstove = "Deep Cleaning"
        else :
            print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Cleaning")
            jstove = "Cleaning"
    elif data['sensors']['statusMainState'] == 6 :
        print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Burn OFF")
        jstove = "Burn Off"
    else :
        print(Fore.WHITE + "               Stove                  : " + Fore.YELLOW + "Unknown state")
        jstove = "Unknown Stove State"

    print(Fore.WHITE + "               Room Temperature       : " + Fore.YELLOW + "{} degC".format(data['sensors']['inputRoomTemperature']))
    print(Fore.WHITE + "               Flame Temperature      : " + Fore.YELLOW + "{} degC".format(data['sensors']['inputFlameTemperature']))

    print(Fore.WHITE + "               Pellets consumption    : " + Fore.YELLOW + "{0} Kg ({1} h)".format(
        data['sensors']['parameterFeedRateTotal'],
        data['sensors']['parameterRuntimePellets']))

    pellets_sacs = round((int(data["sensors"]["parameterFeedRateTotal"]) / 15), 2)
    print(Fore.WHITE + "               Pellets nbre de sacs   : " + Fore.YELLOW + str(pellets_sacs) + " sacs")

    print(Fore.WHITE + "               Diag Motor             : " + Fore.YELLOW + "{} %".format(data['sensors']['outputDischargeMotor']))
    print(Fore.WHITE + "               Fan velocity           : " + Fore.YELLOW + "{} rps".format(data['sensors']['outputIDFan']))

    json_data = {"SENSOR":{"check_time": current_time, "stove_status": jstove, "room_temp": int(data["sensors"]["inputRoomTemperature"]), "flame_temp": data["sensors"]["inputFlameTemperature"], "pellets_used": data["sensors"]["parameterFeedRateTotal"], "pellets_time": data["sensors"]["parameterRuntimePellets"], "diag_motor": data["sensors"]["outputDischargeMotor"],"fan_velocity": data["sensors"]["outputIDFan"]}, "STATE":{"stove_status": jstovectl, "revision_date": time.strftime("%d/%m/%Y"), "revision_time": time.strftime("%H:%M"), "operating_mode": jstovemode, "target_temp": int(data["controls"]["targetTemperature"]), "protection_temp": data["controls"]["setBackTemperature"]}}
    #print(json.dumps(json_data, sort_keys=True, indent=2))
    with open(json_path, 'w') as text_file:
        #print(json_data, file=text_file)
        print(json.dumps(json_data, sort_keys=True), file=text_file)
    return json_data

def get_stove_consumption(data) :
    return data['sensors']['parameterFeedRateTotal']

def get_stove_temperature(data) :
    return data['sensors']['inputFlameTemperature']

def get_stove_thermostat(data) :
    return data['controls']['targetTemperature']

def get_room_temperature(data) :
    return data['controls']['targetTemperature']

def is_stove_burning(data) :
    if data['sensors']['statusMainState'] == 4 or data['sensors']['statusMainState'] == 5 :
        return True
    else :
        return False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print(Fore.WHITE + "                                      : " + Fore.GREEN + "Connected!" + Fore.RESET)
    else:
        print(Fore.RED + "               Bad connection Returned code=" + Fore.RESET,rc)

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in=json.loads(m_decode)

if __name__ == "__main__":

    config_file = Path(os.path.dirname(__file__) + "/rika_config.yaml")
    #print('basename:    ', os.path.basename(__file__))
    #print('dirname:     ', os.path.dirname(__file__))

    if config_file.exists():
        config = load_config(config_file)

    else:
        error_text = """
        The configuration file is missing !
        Please create the following file:
        
        Name : rika_config.yaml

        Add the following items (and fill the missing data):

        system:
            url_base: 'https://www.rika-firenet.com'
            url_login: '/web/login'
            url_stove: '/web/stove/'
            url_api: '/api/client/'
            json_path: ''
            verbose: ''
            verbose_extended: ''

        user:
            username: ''
            password: ''

        mqtt:
            server_address: ''
            topic: ''
            client: ''
            client_username: ''
            client_password: ''
        """
        print(error_text)
        exit()

    user = config['user']['username']
    pwd = config['user']['password']
    current_time = datetime.datetime.now().date().strftime("%d.%m.%y") + " " + datetime.datetime.now().time().strftime("%H:%M")
    url_base = config['system']['url_base']
    url_login = config['system']['url_login']
    url_stove = config['system']['url_stove']
    url_api = config['system']['url_api']
    json_path = config['system']['json_path']
 
    client = requests.session()
    client.verify = False

    print(Fore.CYAN + "Information : ")
    print(Fore.WHITE + "               Starting Rika Update (" + current_time + ")")
    print(Fore.WHITE + "               Connecting to Firenet...")
    stove = connect(client, url_base, url_login, url_stove, user, pwd)

    if len(stove) == 0 :
        print(Fore.RED + "               No RIKA found (connection failed ?)" + Fore.RESET)
        sys.exit(1)

    # Get information
    stove_infos = get_stove_information(client, url_base, url_api, stove)
    stove_json = show_stove_information(stove_infos)

    # Send MQTT
    mqtt_server = config['mqtt']['server_address']
    # Converting to JSON
    data_out = json.dumps(stove_json, sort_keys=True)
    # Process
    topic = config['mqtt']['topic']
    # Create flag in class
    mqtt.Client.connected_flag=False
    client=mqtt.Client(config['mqtt']['client'])
    client.username_pw_set(username=config['mqtt']['client_username'],password=config['mqtt']['client_password'])
    # Bind call back function
    client.on_connect=on_connect
    client.on_message=on_message
    print(Fore.CYAN + "MQTT :")
    print(Fore.WHITE + "               Connecting to broker   :" + Fore.RESET, mqtt_server)
    client.connect(mqtt_server)
    client.loop_start()
    client.subscribe(topic)
    time.sleep(3)
    print("               Sending MQTT data      : Please wait...")
    client.publish(topic,data_out)
    print(Fore.WHITE + "                                      : " + Fore.GREEN + "MQTT Sent" + Fore.RESET)
    time.sleep(5)
    client.loop_stop()
    client.disconnect()
    print(Fore.CYAN + "Process done !" + Fore.RESET)
    # To display result of the API, uncomment following line
    if config['system']['verbose'] == "True":
        print("")
        print("JSON CONTENT (RESULT OF DATA RETRIEVAL)")
        print("----------------------------------------------------------------------------------------------")
        print(stove_infos)
        print("----------------------------------------------------------------------------------------------")
        if config['system']['verbose_extended'] == 'True':
            print("")
            print("HTML CONTENT FROM RIKA WEBSITE")
            print("----------------------------------------------------------------------------------------------")
            print(web_response)
            print("----------------------------------------------------------------------------------------------")
