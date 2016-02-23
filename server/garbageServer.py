'''*********************************************************************************
SERVER - GARBAGE BIN
*********************************************************************************'''
#Import the Modules Required
import paho.mqtt.client as mqtt
from pubnub import Pubnub
import ConfigParser
import logging
import json  
#Importing the Config File and Parsing the file using the ConfigParser
config_file = "./config.ini"
Config = ConfigParser.ConfigParser()
Config.read(config_file)
logging.basicConfig(filename='logger.log',level=logging.DEBUG)

'''****************************************************************************************

Function Name 	:	ConfigSectionMap
Description		:	Parsing the Config File and Extracting the data and returning it
Parameters 		:	section - section to be parserd

****************************************************************************************'''
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            logging.debug("exception on %s!" % option)
            dict1[option] = None
    return dict1 

# Initialize the Pubnub Keys 
PUB_KEY = ConfigSectionMap("pubnub_init")['pub_key']
SUB_KEY = ConfigSectionMap("pubnub_init")['sub_key']

# Initialize the MQTT 
HOST_IP = ConfigSectionMap("mqtt_init")['host_ip']
CHANNEL_OBJECT = "garbaseData"

'''****************************************************************************************

Function Name 	:	on_connect
Description		:	The callback for when the client receives a CONNACK response 
					from the server.
Parameters 		:	client - client id
					rc - flag

****************************************************************************************'''
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(CHANNEL_OBJECT)


'''****************************************************************************************

Function Name 	:	on_message
Description		:	The callback for when a PUBLISH message is received from the server.
Parameters 		:	client - client id
					msg = message received from the client

****************************************************************************************'''
# 
def on_message(client, userdata, msg):
	message = dict()
	message = json.loads(msg.payload)  
	print pubnub.publish(channel="garbageApp-resp", message=message)

'''****************************************************************************************

Function Name 	:	init
Description		:	Initalize the MQTT Protocol, pubnub keys and Starts Subscribing 
					from the garbageApp-req channels
Parameters 		:	None

****************************************************************************************'''
def init():
	#Pubnub Initialization
	global pubnub,client 
	pubnub = Pubnub(publish_key=PUB_KEY,subscribe_key=SUB_KEY)
	pubnub.subscribe(channels='garbageApp-req', callback=appcallback, error=appcallback, reconnect=reconnect, disconnect=disconnect)
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(HOST_IP, 1883, 60)

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	client.loop_forever()
	
'''****************************************************************************************

Function Name 	:	appcallback
Description		:	Waits for the Request sent from the APP 
Parameters 		:	message - Request sent from the app
					channel - channel for the appcallback

****************************************************************************************'''
def appcallback(message, channel):
	if(message.has_key("requester") and message.has_key("requestType")):
		if(message["requestType"] == 0):
			appResponse(message["requester"],message["requestType"])
	else:
		pass

'''****************************************************************************************

Function Name 	:	error
Description		:	If error in the channel, prints the error
Parameters 		:	message - error message

****************************************************************************************'''
def error(message):
    logging.debug("ERROR : " + str(message))

'''****************************************************************************************

Function Name 	:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message

****************************************************************************************'''
def reconnect(message):
    logging.info("RECONNECTED")

'''****************************************************************************************

Function Name 	:	disconnect
Description		:	Responds if server disconnects from pubnub
Parameters 		:	message

****************************************************************************************'''
def disconnect(message):
    logging.info("DISCONNECTED")
	

if __name__ == '__main__':
	#Initialize the Script
	init()



#End of the program