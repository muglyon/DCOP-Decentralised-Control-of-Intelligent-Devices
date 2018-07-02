#!/bin/sh
sudo az iot hub create --resource-group IoTEdge --name slh-iot-hub --sku F1
sudo az iot hub device-identity create --device-id camera --hub-name slh-iot-hub --edge-enabled
sudo ./install_iotedgectl.sh
