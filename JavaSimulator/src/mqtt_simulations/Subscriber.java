package mqtt_simulations;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import utils.Constantes;

/***
 * mqtt_simulations Subscriber based on RaspberryPi mqtt_simulations Server
 * This can be useful to test the state of the server.
 * IT IS NOT MEANT TO BE USED IN THE FINAL APP !
 */
public class Subscriber {

    public static void main(String[] args) {

        System.out.println("RUNNING THE SUBSCRIBER (SERVER ?) --------------");

        try {
            MqttClient client = new MqttClient(Constantes.RASPBERRY_MQTT_SERVER_ADRESS, MqttClient.generateClientId());
            client.setCallback( new SimpleMqttCallBack() );
            client.connect();
            client.subscribe(Constantes.MQTT_ROOT_TOPIC);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
