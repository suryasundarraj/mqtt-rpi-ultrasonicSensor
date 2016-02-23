'''*********************************************************************************
CLIENT - GARBAGE BIN
*********************************************************************************'''
#Import the Modules Required
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

#Constants to be initialized 
GARBAGE_ID = "001"
#Trigger Pin to be connected to the GPIO 23
TRIG = 23 
#Echo Pin to be connected to the GPIO 24
ECHO = 24

'''****************************************************************************************

Function Name 	:	init
Description		:	Initalize the MQTT Protocol and connect to the host
Parameters 		:	None

****************************************************************************************'''
def init():
	global mqttc
	mqttc = mqtt.Client("python_pub")
	mqttc.connect("192.168.1.224", 1883)

'''****************************************************************************************

Function Name 	:	ultrasonicSensor_init
Description		:	Initalize the pins and set the Board Pins to BCM "Broadcom SOC channel"
Parameters 		:	None

****************************************************************************************'''
def ultrasonicSensor_init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.output(TRIG, False)
	
'''****************************************************************************************

Function Name 	:	distanceMeasurement
Description		:	Deducts the Distace and publishes to the MQTT Broker 
Parameters 		:	None

****************************************************************************************'''
def distanceMeasurement():
	prev_distance = 0
	while 1:
		ultrasonicSensor_init()
		time.sleep(2)		
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		#Starts the timer 
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		#Waits for the timer to end once the pin is high
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150

		distance = round(distance, 2)

		if(prev_distance != distance and prev_distance > (distance+3) or prev_distance < (distance-3)):
			prev_distance = distance
			mqttc.publish("garbaseData", "{\"container\":\""+GARBAGE_ID+"\",\"level\":"+str(distance)+"}")
		print "Distance:",distance,"cm"
		GPIO.cleanup()

#Main - Script starts from here
if __name__ == '__main__':
	#Initialize the Script
	init()
	distanceMeasurement()

#End of the program