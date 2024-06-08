import paho.mqtt.client as mqtt
import time
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_DHT
import random
import math
DHT11=Adafruit_DHT.DHT11  


# Initialising Lcd and giving out the pin number in the arguements
lcd = Adafruit_CharLCD(rs = 26, en = 19, d4 = 13, d5 = 6, d6 = 5, d7 = 11, cols = 20, lines=3)

# Clearing out the lcd screen
lcd.clear()

loop = -1

# On connection with broker execute the following function
def on_connect(client, u, f, r):
    print(f"Connected with result code {r}")
    
    #Subscribing to topic "raspberry/model"
    client.subscribe("raspberry/model")

# On getting a message execute the following function
def on_message(client, userdata, msg):
    global loop
    if loop == -1:
        loop = 0
        return
    
    # Decoding payload from the received message
    flow = float(msg.payload.decode())
    
    # Converting flow to 2 decimal precision and then string
    flow = '{0:.2f}'.format(flow)
    flow = str("Flow : " + flow + " %")
    
    # Printing flow to lcd
    lcd.message(flow)
    
    # Printing for testing purpose
    print('Flow : ', flow)
    
    # Waiting 
    sleep(1)
    
    # Setting cursor to next row, 0th column
    lcd.show_cursor(True)
    lcd.set_cursor(0, loop+1)
    loop += 1

# setting client
client = mqtt.Client()

# setting callback methods
client.on_connect = on_connect
client.on_message = on_message

# connecting to broker
client.connect("broker.emqx.io", 1883, 60)


for i in range(3):
    # Taking sensor reading
    temp,humid=Adafruit_DHT.read_retry(DHT11,21)
    
    #temp = random.randint(20, 30)
    #humid = random.randint(40, 70)
    
    # Forming payload
    p = str(temp)+ ' ' +str(humid)
    
    # Publishing message
    client.publish('raspberry/topic', payload=p, qos=0, retain=False)
    
    # Testing output
    print(f"send {i} to raspberry/topic")
    

client.loop_forever()

