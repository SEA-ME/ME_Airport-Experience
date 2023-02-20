import random

from paho.mqtt import client as mqtt_client
import os
import asyncio
import json
from azure.iot.device import IoTHubDeviceClient


broker = '192.168.218.196'
port = 1883
topic = "my_robot1234tayyab"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
message = " "

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
   # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        result = json.loads(msg.payload.decode())
        msg = json.dumps(result[-1])
        # Fetch the connection string from an environment variable
        conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
        device_id = os.getenv("DEVICE_ID")

        # Create instance of the device client using the authentication provider
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        # Connect the device client.
        device_client.connect()
        # Send a single message
        print("Sending message...")

        device_client.send_message(msg)

        print("Message successfully sent:", msg)

        # finally, shut down the client
        device_client.shutdown()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()





if __name__ == '__main__':
    run()
