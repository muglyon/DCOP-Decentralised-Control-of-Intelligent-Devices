package core;

import utils.Constantes;

import java.util.ArrayList;
import java.util.List;

/***
 * An agent = a room
 */
public class Room {

    private static int NB_AGENTS = 1;

    private int id;
    private int tau; //temps depuis le dernier passage de l'infirmière
    private int priority;
    private int previous_vi; //vi précédemment donné par l'algo
    private Room leftNeighbor;
    private Room rightNeighbor;
    private Room frontNeighbor;
    private List<Device> devices;

    /***
     * Generate random room environment
     */
    public Room() {
        id = NB_AGENTS;
        NB_AGENTS++;

        tau = (int) (Math.random() * Constantes.INFINITY);
        previous_vi = (int) (Math.random() * tau);
        priority = previous_vi < 30 ? 1 : 0;
        leftNeighbor = null;
        rightNeighbor = null;
        frontNeighbor = null;
        devices = new ArrayList<Device>();

        int deviceId = 1;
        for (int i = 0; i < (int) (Math.random() * (Constantes.MAX_NB_DEVICES)); i++) {
            devices.add(new Device(id, deviceId));
            deviceId++;
        }
    }

    public Room(int id, int tau, List<Device> devices) {
        this.id = id;
        this.tau = tau;
        this.priority = 0;
        this.previous_vi = Constantes.INFINITY;
        this.leftNeighbor = null;
        this.rightNeighbor = null;
        this.frontNeighbor = null;
        this.devices = devices;
    }

    public Room(int id, int tau) {
        this.id = id;
        this.tau = tau;
        this.priority = 0;
        this.previous_vi = Constantes.INFINITY;
        this.leftNeighbor = null;
        this.rightNeighbor = null;
        this.frontNeighbor = null;
        this.devices = new ArrayList<Device>();
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getTau() {
        return tau;
    }

    public void setTau(int tau) {
        this.tau = tau;
    }

    public Room getLeftNeighbor() {
        return leftNeighbor;
    }

    public void setLeftNeighbor(Room leftNeighbor) {
        this.leftNeighbor = leftNeighbor;
    }

    public Room getRightNeighbor() {
        return rightNeighbor;
    }

    public void setRightNeighbor(Room rightNeighbor) {
        this.rightNeighbor = rightNeighbor;
    }

    public Room getFrontNeighbor() {
        return frontNeighbor;
    }

    public void setFrontNeighbor(Room frontNeighbor) {
        this.frontNeighbor = frontNeighbor;
    }

    public List<Device> getDevices() {
        return devices;
    }

    public void setDevices(List<Device> devices) {
        this.devices = devices;
    }

    public int getPriority() {
        return priority;
    }

    public void increasePriority() {
        this.priority++;
    }

    public void setLowerPriority() {
        this.priority = 0;
    }

    public int getPrevious_vi() {
        return previous_vi;
    }

    public void setPrevious_vi(int previous_vi) {
        this.previous_vi = previous_vi;
    }

    /***
     * Set +minutes to all the prevision times
     * @param minutes
     */
    public void incrementTime(int minutes) {
        tau += minutes;
        previous_vi -= minutes;

        for(Device device : devices) {
            if(device.getEndOfProgram() > 0) {
                device.setEndOfProgram(device.getEndOfProgram() - minutes);
            }
        }
    }

    /***
     * Check if the room as at least one device connected
     * @return
     */
    public boolean hasNoDevices() {
        return devices.size() == 0;
    }

    /***
     * Check if one of the devices is in critical state
     * @return
     */
    public boolean hasEmergency() {
        for(Device device : devices) {
            if(device.isInCriticalState()) {
                return true;
            }
        }
        return false;
    }

    /***
     * Check if tau is greater then 180 (if the patient is using more then 5 devices),
     * or greater then 210 (else)
     * @return
     */
    public boolean isTauToBig() {
        return (devices.size() > 5 && tau >= 180) || (devices.size() >= 1 && tau >= 210);
    }

    /***
     * Check is neighboor with room
     * @param room
     * @return
     */
    public boolean hasForNeighboor(Room room) {
        return (leftNeighbor == null ? false : leftNeighbor.equals(room))
                || (rightNeighbor == null ? false : rightNeighbor.equals(room))
                || (frontNeighbor == null ? false : frontNeighbor.equals(room));
    }

    public boolean equals(Room room) {
        return room.id == id;
    }

    /***
     * Check that the device need an intervention (for priority constraint)
     * @return
     */
    public boolean needIntervention() {
        return !hasEmergency() && !hasNoDevices() && (getTimeWhenFirstDeviceWillEnd() < 30 || isTauToBig());
    }

    /***
     * Get the number of minutes left before the next predictable intervention on a device
     * @return
     */
    public int getTimeWhenFirstDeviceWillEnd() {
        int timeFirstDeviceWillEnd = -1;
        for(Device device : devices) {
            if(timeFirstDeviceWillEnd == -1 || timeFirstDeviceWillEnd > device.getEndOfProgram()) {
                timeFirstDeviceWillEnd = device.getEndOfProgram();
            }
        }
        return timeFirstDeviceWillEnd;
    }

    public String toString() {
        String result = "ROOM " + id + " : \n"
                + "| Dernier passage : " + tau + "\n"
                + "| Priorité : " + priority + "\n"
                + "| vi Précédent : " + previous_vi + "\n";

        for(Device device : devices) {
            result = result + device.toString();
        }

        return result;
    }
}
