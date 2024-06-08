import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import activations
import matplotlib.pyplot as plt
from paho.mqtt import client as mqtt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from keras.models import load_model
import time


i = -1

# Reading CSV file
data = pd.read_csv('IOT_Assignment_2_data_regression_sensor_range.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# Loading model
ann = load_model('Final_IOT_Model.h5')

# ann = tf.keras.models.Sequential()
# ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
# ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
# ann.add(tf.keras.layers.Dense(units=1))
# custom_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
# ann.compile(optimizer = custom_optimizer, loss = 'mean_squared_error')
# ann.fit(X_train, y_train, epochs = 100)
y_pred = ann.predict(X_test)
R2 = r2_score(y_test, y_pred, multioutput='variance_weighted')
print(R2)

# Function to execute on connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Subscribe to topic "raspberry/topic"
        

def on_message(client, userdata, msg):
    global i 
    if(i == -1):
        i = 0
        return

    # Taking out temp and humidity in list
    li = msg.payload.decode().split()

    # Initialising temp and humid with there respective values
    temp = float(li[0])
    humid = float(li[1])

    # Testing output
    print('Temp : ', temp, ' Humid : ', humid)

    # Predicting the water flow percentage
    x = str(ann.predict([[humid, temp]])[0][0])

    # Testing output
    print('Prediction : ', x)

    # Publishing the waterflow
    client.publish('raspberry/model', payload = x, qos=1, retain=True)
    
    i += 1
    print("sending water flow")
    print()

# setting client
client = mqtt.Client()

# setting callback methods
client.on_connect = on_connect
client.on_message = on_message


# connecting to broker
client.connect("broker.emqx.io", 1883, 60)

client.loop_forever()
