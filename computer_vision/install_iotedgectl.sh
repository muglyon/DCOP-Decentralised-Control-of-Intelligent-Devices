#!/bin/sh
sudo pip3 uninstall -y azure-iot-edge-runtime-ctl
sudo pip3 install azure-iot-edge-runtime-ctl

sudo iotedgectl setup --connection-string "HostName=slh-iot-hub.azure-devices.net;DeviceId=camera;SharedAccessKey=aOt7x53Z71xbRoTzAi5KBspgpgKlE0goHcQY5gJr8KU=" --auto-cert-gen-force-no-password
sudo iotedgectl login --address slhcontainerregistry.azurecr.io --username slhContainerRegistry --password pANk+7LjgElYs84UQKgvDr+jFypLe3KP