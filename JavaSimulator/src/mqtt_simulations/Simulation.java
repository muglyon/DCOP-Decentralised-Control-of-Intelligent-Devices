package mqtt_simulations;

import com.google.gson.Gson;
import core.Device;
import core.Hospital;
import core.Room;
import org.eclipse.paho.client.mqttv3.*;
import utils.Constantes;

/***
 * Send some devices informations to the MQTT Server
 */
public class Simulation {

    public static void main(String[] args) {

        Hospital hospital = new Hospital(10);

        //while(true) {

            for (Room room : hospital.getRooms()) {
                for (Device device : room.getDevices()) {

                    try {

                        MqttMessage message = new MqttMessage();
                        message.setPayload(new Gson().toJson(device).getBytes());

                        MqttClient client = new MqttClient(
                                Constantes.RASPBERRY_MQTT_SERVER_ADRESS,
                                MqttClient.generateClientId(),
                                null);

                        client.connect();
                        client.publish(Constantes.MQTT_ROOT_TOPIC + "/" + room.getId(), message);
                        client.disconnect();
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }

            /*try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }*/
        //}
    }
}
