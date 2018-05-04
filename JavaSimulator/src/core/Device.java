package core;

import com.google.gson.Gson;
import utils.Constantes;

/***
 * core.Device simulated
 */
public class Device {

    private int id;
    private int endOfProgram; //temps avant la fin du programme
    private boolean isInCriticalState;

    /***
     * Generate random device environment
     */
    public Device(int agentId, int id) {
        this.id = Integer.parseInt(agentId + "" + id);
        endOfProgram = (int)(Math.random() * (Constantes.INFINITY - 5)) + 5; //valeurs entre 5 et 241
        isInCriticalState = ((int)(Math.random() * 99) + 1) < 5 ? true : false;
    }

    public Device(int id, int endOfTheProgram, boolean isInCriticalState) {
        this.id = id;
        this.endOfProgram = endOfTheProgram;
        this.isInCriticalState = isInCriticalState;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getEndOfProgram() {
        return endOfProgram;
    }

    public void setEndOfProgram(int endOfProgram) {
        this.endOfProgram = (endOfProgram < 0) ? 0 : endOfProgram;
    }

    public boolean isInCriticalState() {
        return isInCriticalState;
    }

    public void setInCriticalState(boolean inCriticalState) {
        isInCriticalState = inCriticalState;
    }

    public String toString() {
        String result = " > core.Device " + id + " ";
        result = result + (isInCriticalState ? "is in critical STATE !\n" : "end it's program in " + endOfProgram +"\n");
        return result;
    }
}
