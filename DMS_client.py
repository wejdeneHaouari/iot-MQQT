import paho.mqtt.client as mqtt
import threading
from datetime import datetime


class MDMS(mqtt.Client):

    def __init__(self):
        self.id = "MSMS_client"
        self.client = mqtt.Client(self.id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.port = 1883
        self.domain = "localhost"

    def connect(self):
        self.client.connect(self.domain, self.port, 60)
        self.price()
        self.reduction()
        self.client.loop_forever()

    def price(self, price=500):
        self.client.publish("price", qos=0, payload=price)
        # price is published once every 60 min
        threading.Timer(60.0 * 60, self.price).start()

    def reduction(self, reduction=10):
        self.client.publish("reduction", qos=2, payload=reduction)
        # reduction is published every minute
        threading.Timer(60.0, self.reduction).start()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("production")
        client.subscribe("consummation")

    @staticmethod
    def on_message(client, userdata, msg):
        now = datetime.now()
        current_time = now.ctime()
        print(current_time + " " + msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    mdms = MDMS()
    mdms.connect()
