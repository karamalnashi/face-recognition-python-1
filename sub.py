import paho.mqtt.client as mqttclient
import time

import face_recognition
from PIL import Image, ImageDraw
import face_recognition as fr
import cv2
import os
from imutils import paths
import indentify
import numpy as np


def on_connect(client , userdata,flags,rc):
    if rc ==0:
        print("client is connected")
        client.subscribe("search")
        client.subscribe("Training")
        client.subscribe("name")
        
        global connected
        #connected=True
    else:
        print("client is error")


def on_message (client,userdata,message):
    print("message recieved = "+str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)

    if message.topic== "search":
        fh = open("test.jpg", "wb")
        fh.write(base64.b64decode((message.payload)))
        indentify.classify_face("test.jpg")
        with open("identify.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        client.publish("sub",encoded_string)
    elif message.topic== "Training":
        fh = open("./known/test.jpg", "wb")
        fh.write(base64.b64decode((message.payload)))
        time.sleep(0.2)
        indentify.unknown_image_encoded("test.jpg")
    else:
        old_file_name = "./known/test.jpg"
        new_file_name = "./known/"+str(message.payload.decode("utf-8"))+".jpg"
        os.rename(old_file_name, new_file_name)
        indentify.unknown_image_encoded(str(message.payload.decode("utf-8"))+".jpg")

    

    
Messagerecieved=False
#connected=False

broker_address ="hairdresser.cloudmqtt.com"
port=16484
user="pcpvemdw"
password="OzRXPA2Itqzm"

client = mqttclient.Client("MQTT")
client.on_message= on_message
client.username_pw_set(user, password=password)
client.on_connect=on_connect
client.connect(broker_address,port=port)

client.loop_forever()