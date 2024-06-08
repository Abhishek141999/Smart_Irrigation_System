import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import activations
import matplotlib.pyplot as plt
from paho.mqtt import client as mqtt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import time

i = -1

data = pd.read_csv('IOT_Assignment_2_data_regression_sensor_range.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
ann.add(tf.keras.layers.Dense(units=1))
custom_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
ann.compile(optimizer = custom_optimizer, loss = 'mean_squared_error')
ann.fit(X_train, y_train, epochs = 100)
y_pred = ann.predict(X_test)
R2 = r2_score(y_test, y_pred, multioutput='variance_weighted')
print(R2)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("raspberry/topic")

def on_message(client, userdata, msg):
    global i 
    if(i == -1):
        i = 0
        return
    # print(f"Received temperature and Humidity where msg no : ", msg.payload.decode())
    # p = str(msg.payload)
    # print(p)
    li = msg.payload.decode().split()
    temp = int(li[0])
    humid = int(li[1])
    print('Temp : ', temp, ' Humid : ', humid)
    x = ann.predict([[temp, humid]])
    x = str(x[0][0])
    print('Prediction : ', x)
    client.publish('raspberry/model', payload = x, qos=0, retain=True)
    i += 1
    print("sending water flow")
    print()
    # time.sleep(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.will_set('raspberry/status', b'{"status": "Off"}')

client.connect("broker.emqx.io", 1883, 60)
# print(li)
client.loop_forever()
