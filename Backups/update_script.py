import paho.mqtt.client as mqtt
import netifaces as ni
import git


MQTT_SERVER = "10.33.120.194"
MY_IP = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

def on_connect(client, userdata, flags, rc):
    """
    CallBack MQTT Connection
    """
    client.subscribe("DCOP/" + str(MY_IP))
    print("subscribe to : ", "DCOP/" + str(MY_IP))


def on_message(client, userdata, msg):
    """
    CallBack Message Arrive
    - Update the Git repository
    """
    git.cmd.Git("DCOP/").pull()
    print("PULL GIT")


def on_disconnect(client, userdata, rc=0):
    """
    CallBack when disconnection
    """
    print("Disconnected result code :", rc)
    client.loop_stop()


if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()