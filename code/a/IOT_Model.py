import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import activations
import matplotlib.pyplot as plt
 
 
data = pd.read_csv('IOT_Assignment_2_data_regression_sensor_range.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
 
 
t1 = X[:,0]
plt.scatter(t1,y)
t2 = X[:,1]
plt.scatter(t2,y)
plt.scatter(t1,t2)
 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
 
ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
ann.add(tf.keras.layers.Dense(units=4, activation='relu'))
ann.add(tf.keras.layers.Dense(units=1))
 
custom_optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
ann.compile(optimizer = custom_optimizer, loss = 'mean_squared_error')
 
ann.fit(X_train, y_train, epochs = 400)
 
from sklearn.metrics import r2_score
y_pred = ann.predict(X_test)
R2 = r2_score(y_test, y_pred, multioutput='variance_weighted')
 
#R2 score is used as avaulation matics 
print("R2 score :" , R2)
 
#weigths povided by Input layer layer
ann.layers[0].weights[0]
 
#weigths povided by First Hidden layer layer
ann.layers[1].weights[0]
 
#weigths povided by Second Hidden layer layer
ann.layers[2].weights[0]
 