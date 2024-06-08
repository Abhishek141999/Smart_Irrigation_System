# python3.6

import random
import numpy as np
import pandas as pd
# import tensorflow as tf
# from tensorflow.keras import activations
import matplotlib.pyplot as plt
from paho.mqtt import client as mqtt_client
# from sklearn.metrics import r2_score
# from sklearn.model_selection import train_test_split
import time


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
topic2 = "python/send"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'

# data = pd.read_csv('IOT_Assignment_2_data_regression_sensor_range.csv')
# X = data.iloc[:, :-1].values
# y = data.iloc[:, -1].values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
# ann = tf.keras.models.Sequential()
# ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
# ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
# ann.add(tf.keras.layers.Dense(units=1))
# custom_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
# ann.compile(optimizer = custom_optimizer, loss = 'mean_squared_error')
# ann.fit(X_train, y_train, epochs = 100)
# y_pred = ann.predict(X_test)
# R2 = r2_score(y_test, y_pred, multioutput='variance_weighted')
# print(R2)


def publish(client):
    msg_count = 0
    for i in range(5):
        time.sleep(1)
        msg = "predicted Val"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        p = msg.payload.decode().split(' ')
        temp = p[0]
        humid = p[1]
        print(temp, humid)
        # print('trying to publish')
        
        


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    # publish(client)
    client.loop_forever()



if __name__ == '__main__':
    run()