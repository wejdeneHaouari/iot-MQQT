import paho.mqtt.client as mqtt
import threading
from datetime import datetime


class SM(mqtt.Client):
    def __init__(self):
        self.id = "SM_client"
        self.client = mqtt.Client(self.id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.port = 1883
        self.domain = "localhost"

    def connect(self):
        self.client.connect(self.domain, self.port, 60)
        self.consummation()
        self.production()
        self.client.loop_forever()

    def consummation(self, consummation=10):
        self.client.publish("consummation", payload=consummation, qos=2)
        threading.Timer(60.0 * 6, self.consummation).start()

    def production(self, production=2):
        self.client.publish("production", payload=production, qos=2)
        threading.Timer(60.0 * 2, self.production).start()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code: {}".format(rc))
        client.subscribe("reduction")
        client.subscribe("price")

    @staticmethod
    def on_message(client, userdata, msg):
        now = datetime.now()
        current_time = now.ctime()
        print(current_time + " " + msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    sm = SM()
    sm.connect()
