About codes -

	-> Code to train model and send waterflow percentage : 
		-> It contains the code which runs on our machine to calculate waterflow percentage using model and send it back to the subscriber to print in the lcd.
    	-> It acts as both subscriber and publisher
    	-> It subscribes topic 'raspberry/topic' to get temperature and humidity
    	-> After that it runs perceptron model to calculate the water flow percentage
    	-> Then it publishes the water flow percentage in the topic 'raspberry/model'. 

    -> Code to send temp, Humidity data and show water flow percentage in lcd : 
    	-> It contains the code which runs on raspberrypi os.
    	-> It has the code of sensor and lcd.
    	-> It also acts as both subscriber and publisher.
    	-> In the sensor code it senses the temperature and humidity.
    	-> Then it publishes the data under topic 'raspberry/topic'.
    	-> It subscribes for topic 'raspberry/model' to receive the waterflow percentage.
    	-> It then shows the waterflow percentage in the lcd

About Zip file -

	-> It contains three file - IOT_Model.py, TheToaster.pdf, readme.txt
	-> IOT_Model.py contains the machine learning code.
	-> TheToaster.pdf file contains the Report for the Assignment.

    	

    