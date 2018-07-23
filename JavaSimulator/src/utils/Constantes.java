package utils;

public class Constantes {

    public static final int INFINITY = 241;
    public static final int MAX_NB_DEVICES = 6;
    public static final int NEXT_TIME_STEP = 10; //10 mins avant le prochain calcul
    public static final int NB_AGENTS = 2; //=> nombre pair uniquement pris en charge pour le moment

    public static final boolean CLEAN_AFTERWARDS = false;

    public static final String AGENT_XML_FILE = "xmlFiles/myDPOPJaCoPAgent.xml";
    public static final String PROBLEM_XML_FILE = "xmlFiles/problemGenerated.xml";
    public static final String RASPBERRY_MQTT_SERVER_ADRESS = "tcp://10.33.120.195:1883";
    public static final String MQTT_ROOT_TOPIC = "DCOP";

    public static final Long TIMEOUT = (long) 960000; //16 minutes
}
