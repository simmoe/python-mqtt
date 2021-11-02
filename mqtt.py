# python 3.6

import random
import time
import ssl
import sys
from paho.mqtt import client as mqtt_client
import psutil    
import pyautogui
import keyboard

from time import sleep

obs_running = "obs64.exe" in (p.name() for p in psutil.process_iter())
print("OBS running: " + str (obs_running) )

broker = 'mqtt.nextservices.dk'
port = 8883
topic = "recording"
# generate client ID with pub prefix randomly
client_id = 'k2-recording-pc'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.tls_set_context(context=None)
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
            time.sleep(2)
            msg_count += 1
"""        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
 """
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if(obs_running):
            if(msg.payload.decode() == 'start' or msg.payload.decode() == 'stop'):
                x, y = pyautogui.position()
                pyautogui.click(x=100, y=-400)
                keyboard.press_and_release('alt+shift+å')
                pyautogui.moveTo(x, y)

            if(msg.payload.decode() == 'scene1'):
                x, y = pyautogui.position()
                pyautogui.click(x=100, y=-400)
                keyboard.press_and_release('alt+shift+1')
                pyautogui.moveTo(x, y)
            if(msg.payload.decode() == 'scene2'):
                x, y = pyautogui.position()
                pyautogui.click(x=100, y=-400)
                keyboard.press_and_release('alt+shift+2')
                pyautogui.moveTo(x, y)
            if(msg.payload.decode() == 'scene3'):
                x, y = pyautogui.position()
                pyautogui.click(x=100, y=-400)
                keyboard.press_and_release('alt+shift+3')
                pyautogui.moveTo(x, y)


    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    print('loop started')
    subscribe(client)
    publish(client)


if __name__ == '__main__':
    run()