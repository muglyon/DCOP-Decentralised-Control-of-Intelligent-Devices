package core;

import java.util.ArrayList;
import java.util.List;

/***
 * Simulated Environnement
 */
public class Hospital {

    private List<Room> rooms;

    public Hospital(List<Room> rooms) {
        this.rooms = rooms;
    }

    /***
     * Generate random hospital environment
     * @param nbAgents
     */
    public Hospital(int nbAgents) {

        rooms = new ArrayList<Room>();

        for(int i = 0; i < nbAgents; i++) {
            rooms.add(new Room());
        }

        //Setup des voisins sur 2 lignes !...
        int moitieAgents = nbAgents / 2;
        List<Room> leftSide = rooms.subList(0, moitieAgents);
        List<Room> rightSide = rooms.subList(moitieAgents, rooms.size());

        for(int k = 0; k < moitieAgents; k++) {
            Room leftCurrent = leftSide.get(k);
            Room rightCurrent = rightSide.get(k);

            if(k == 0) {
                leftCurrent.setLeftNeighbor(rightCurrent);
                rightCurrent.setLeftNeighbor(leftCurrent);
            }

            if(k > 0) {
                leftCurrent.setLeftNeighbor(leftSide.get(k - 1));
                rightCurrent.setLeftNeighbor(rightSide.get(k - 1));
            }

            if(k < moitieAgents - 1) {
                leftCurrent.setRightNeighbor(leftSide.get(k + 1));
                rightCurrent.setRightNeighbor(rightSide.get(k + 1));
            }

            if(k == moitieAgents - 1) {
                leftCurrent.setRightNeighbor(rightCurrent);
                rightCurrent.setRightNeighbor(leftCurrent);
            }

            if(k > 0 && k < moitieAgents - 1) {
                leftCurrent.setFrontNeighbor(rightCurrent);
                rightCurrent.setFrontNeighbor(leftCurrent);
            }
        }
    }

    public List<Room> getRooms() {
        return rooms;
    }

    public void setRooms(List<Room> agents) {
        this.rooms = agents;
    }

    public String toString() {
        String result = "";
        for(Room room : rooms) {
            result = result + room.toString();
        }
        return result;
    }

    /***
     * Set +minutes to all the prevision times
     * @param minutes
     */
    public void incrementTime(int minutes) {
        for(Room room : rooms) {
            room.incrementTime(minutes);
        }
    }
}
