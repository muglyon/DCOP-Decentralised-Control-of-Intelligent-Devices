# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import json
import os
import random
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError
from multiprocessing import Pool
from camera_capture import CameraCapture

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0
TEMPERATURE_THRESHOLD = 25
TWIN_CALLBACKS = RECEIVE_CALLBACKS = 0

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

# String containing Hostname, Device Id & Device Key & Module Id in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>;ModuleId=<module_id>;GatewayHostName=<gateway>"
CONNECTION_STRING = "[Device Connection String]"

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )


# receive_message_callback is invoked when an incoming message arrives on the specified 
# input queue (in the case of this sample, "input1").  Because this is a filter module, 
# we will forward this message onto the "output1" queue.
def receive_message_callback(message, hubManager):
    global RECEIVE_CALLBACKS
    global TEMPERATURE_THRESHOLD
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    message_text = message_buffer[:size].decode('utf-8')
    print("    Data: <<<{}>>> & Size={:d}".format(message_text, size))
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print("    Properties: {}".format(key_value_pair))
    RECEIVE_CALLBACKS += 1
    print("    Total calls received: {:d}".format(RECEIVE_CALLBACKS))
    data = json.loads(message_text)
    if "machine" in data and "temperature" in data["machine"] and data["machine"]["temperature"] > TEMPERATURE_THRESHOLD:
        map_properties.add("MessageType", "Alert")
        print("Machine temperature {} exceeds threshold {}".format(data["machine"]["temperature"], TEMPERATURE_THRESHOLD))
    hubManager.forward_event_to_output("output1", message, 0)
    return IoTHubMessageDispositionResult.ACCEPTED

# device_twin_callback is invoked when twin's desired properties are updated.
def device_twin_callback(update_state, payload, user_context):
    global TWIN_CALLBACKS
    global TEMPERATURE_THRESHOLD
    print("\nTwin callback called with:\nupdateStatus = {}\npayload = {}\ncontext = {}".format(update_state, payload, user_context))
    data = json.loads(payload)
    if "desired" in data and "TemperatureThreshold" in data["desired"]:
        TEMPERATURE_THRESHOLD = data["desired"]["TemperatureThreshold"]
    if "TemperatureThreshold" in data:
        TEMPERATURE_THRESHOLD = data["TemperatureThreshold"]
    TWIN_CALLBACKS += 1
    print("Total calls confirmed: {:d}\n".format(TWIN_CALLBACKS))

class HubManager(object):

    def __init__(
            self,
            connection_string):
        self.client_protocol = PROTOCOL
        self.client = IoTHubClient(connection_string, PROTOCOL)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        # some embedded platforms need certificate information
        self.set_certificates()

    def set_certificates(self):
        isWindows = sys.platform.lower() in ['windows', 'win32']
        if not isWindows:
            CERT_FILE = os.environ['EdgeModuleCACertificateFile']        
            print("Adding TrustedCerts from: {0}".format(CERT_FILE))
            
            # this brings in x509 privateKey and certificate
            file = open(CERT_FILE)
            try:
                self.client.set_option("TrustedCerts", file.read())
                print ( "set_option TrustedCerts successful" )
            except IoTHubClientError as iothub_client_error:
                print ( "set_option TrustedCerts failed (%s)" % iothub_client_error )

            file.close()

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

def main(connection_string):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        hub_manager = HubManager(connection_string)

        print ( "Starting the IoT Hub Python sample using protocol %s..." % hub_manager.client_protocol )
        # print ( "The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        # while True:
        #     time.sleep(1000)
        custom_Thread = CameraCapture(hub_manager)
        custom_Thread.run()

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    try:
        CONNECTION_STRING = os.environ['EdgeHubConnectionString']

    except Exception as error:
        print ( error )
        sys.exit(1)

    main(CONNECTION_STRING)