package frodo_simulations;

import frodo2.algorithms.Solution;
import frodo2.algorithms.XCSPparser;
import frodo2.algorithms.dpop.DPOPsolver;
import frodo2.algorithms.varOrdering.dfs.DFSgeneration;
import frodo2.gui.DOTrenderer;
import frodo2.solutionSpaces.JaCoP.JaCoPxcspParser;
import core.Device;
import core.Hospital;
import core.Room;
import org.jdom2.Document;
import utils.Constantes;
import utils.XMLWriter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/***
 * Run a specific simulation
 */
public class Simulation {

    public static void main(String[] args) {

        System.out.println("SIMULATION A DIFFERENTS T --------------");

        System.out.println("T = 0 ---------------------------------- ");
        Hospital hospital = initSimulatedEnvironment();
        resolveDCOP(hospital);

        System.out.println("T = 10 ---------------------------------- ");
        hospital = step2(hospital);
        resolveDCOP(hospital);

        System.out.println("T = 20 ---------------------------------- ");
        hospital = step3(hospital);
        resolveDCOP(hospital);

        System.out.println("T = 30 ---------------------------------- ");
        hospital = step4(hospital);
        resolveDCOP(hospital);
    }

    /***
     * Write a xml file based on the hospital environment and resolve the DCOP using Frodo's DPOP
     * @param hospital
     */
    public static void resolveDCOP(Hospital hospital) {
        XMLWriter xmlWriter = new XMLWriter();
        Document agentConfig = null;
        Document problemDoc = null;

        xmlWriter.writeFileFor(hospital);

        try {
            agentConfig = XCSPparser.parse(Constantes.AGENT_XML_FILE, false);
            problemDoc = JaCoPxcspParser.parse(Constantes.PROBLEM_XML_FILE, false);
        } catch (Exception e) {
            System.err.println("ERROR PARSING !\n" + e.getMessage());
        }

        System.out.println("SITUATION DETAILS --------------");
        System.out.println(hospital.toString());

        DPOPsolver dpopSolver = new DPOPsolver(agentConfig);

        System.out.println("PROCESSING BEGIN ------------");

        long startTime = System.currentTimeMillis();
        Solution solution = dpopSolver.solve(problemDoc, Constantes.CLEAN_AFTERWARDS, Constantes.TIMEOUT);
        System.out.println(solution.toString());
        System.out.println("JAVA RUNNING TIME : " + (System.currentTimeMillis() - startTime));

        //Affectation des valeurs vi à chaque agent :
        for(Object entry : solution.getAssignments().entrySet()) {

            String[] assignement = entry.toString().split("=");
            int agentNb = Integer.parseInt(assignement[0].split("v")[1]);
            int value = Integer.parseInt(assignement[1]);

            for(Room room : hospital.getRooms()) {
                if(room.getId() == agentNb) {
                    room.setPrevious_vi(value);
                    if(room.getPrevious_vi() < 30 && value < 30) {
                        room.increasePriority();
                    } else {
                        room.setLowerPriority();
                    }
                    break;
                }
            }
        }

        // Graphes
        new DOTrenderer("DFS Tree : ", DFSgeneration.dfsToString(dpopSolver.getDFS()));
        new DOTrenderer("Graph des Contraintes : ", JaCoPxcspParser.toDOT(problemDoc));
    }

    /***
     * Basé sur la simulation à N = 32
     * @return
     */
    public static Hospital initSimulatedEnvironment() {

        Device d21 = new Device(21, Constantes.INFINITY, true);
        Device d61 = new Device(61, 10, false);
        Device d62 = new Device(62, Constantes.INFINITY, false);
        Device d63 = new Device(63, Constantes.INFINITY, false);
        Device d91 = new Device(91, 20, false);
        Device d92 = new Device(92, 30, false);
        Device d93 = new Device(93, Constantes.INFINITY, false);
        Device d94 = new Device(94, Constantes.INFINITY, false);
        Device d95 = new Device(95, Constantes.INFINITY, false);
        Device d101 = new Device(101, Constantes.INFINITY, false);
        Device d102 = new Device(102, 40, false);
        Device d151 = new Device(151, 5, false);
        Device d152 = new Device(152, Constantes.INFINITY, false);
        Device d153 = new Device(153, Constantes.INFINITY, false);
        Device d161 = new Device(161, Constantes.INFINITY, false);
        Device d221 = new Device(221, Constantes.INFINITY, false);
        Device d231 = new Device(231, Constantes.INFINITY, false);
        Device d232 = new Device(232, Constantes.INFINITY, false);
        Device d261 = new Device(261, 5, false);
        Device d262 = new Device(262, Constantes.INFINITY, false);
        Device d263 = new Device(263, Constantes.INFINITY, false);
        Device d271 = new Device(271, Constantes.INFINITY, false);
        Device d272 = new Device(272, Constantes.INFINITY, false);
        Device d273 = new Device(273, 40, false);
        Device d274 = new Device(274, 40, false);
        Device d311 = new Device(311, 60, false);

        Room a1 = new Room(1, Constantes.INFINITY);
        Room a2 = new Room(2, 220, Arrays.asList(d21));
        Room a3 = new Room(3, Constantes.INFINITY);
        Room a4 = new Room(4, Constantes.INFINITY);
        Room a5 = new Room(5, Constantes.INFINITY);
        Room a6 = new Room(6, 110, Arrays.asList(d61, d62, d63));
        Room a7 = new Room(7, Constantes.INFINITY);
        Room a8 = new Room(8, Constantes.INFINITY);
        Room a9 = new Room(9, 180, Arrays.asList(d91, d92, d93, d94, d95));
        Room a10 = new Room(10, 130, Arrays.asList(d101, d102));
        Room a11 = new Room(11, Constantes.INFINITY);
        Room a12 = new Room(12, Constantes.INFINITY);
        Room a13 = new Room(13, Constantes.INFINITY);
        Room a14 = new Room(14, Constantes.INFINITY);
        Room a15 = new Room(15, 60, Arrays.asList(d151, d152, d153));
        Room a16 = new Room(16, 30, Arrays.asList(d161));
        Room a17 = new Room(17, Constantes.INFINITY);
        Room a18 = new Room(18, Constantes.INFINITY);
        Room a19 = new Room(19, Constantes.INFINITY);
        Room a20 = new Room(20, Constantes.INFINITY);
        Room a21 = new Room(21, Constantes.INFINITY);
        Room a22 = new Room(22, 80, Arrays.asList(d221));
        Room a23 = new Room(23, 190, Arrays.asList(d231, d232));
        Room a24 = new Room(24, Constantes.INFINITY);
        Room a25 = new Room(25, Constantes.INFINITY);
        Room a26 = new Room(26, 5, Arrays.asList(d261, d262, d263));
        Room a27 = new Room(27, 20, Arrays.asList(d271, d272, d273, d274));
        Room a28 = new Room(28, Constantes.INFINITY);
        Room a29 = new Room(29, Constantes.INFINITY);
        Room a30 = new Room(30, Constantes.INFINITY);
        Room a31 = new Room(31, 230, Arrays.asList(d311));
        Room a32 = new Room(32, Constantes.INFINITY);

        a1.setLeftNeighbor(a2);
        a2.setLeftNeighbor(a3);
        a3.setLeftNeighbor(a4);
        a4.setLeftNeighbor(a5);
        a5.setLeftNeighbor(a6);
        a6.setLeftNeighbor(a7);
        a7.setLeftNeighbor(a8);
        a8.setLeftNeighbor(a9);
        a10.setLeftNeighbor(a11);
        a11.setLeftNeighbor(a12);
        a12.setLeftNeighbor(a13);
        a13.setLeftNeighbor(a14);
        a14.setLeftNeighbor(a15);
        a16.setLeftNeighbor(a17);
        a17.setLeftNeighbor(a18);
        a18.setLeftNeighbor(a19);
        a19.setLeftNeighbor(a20);
        a20.setLeftNeighbor(a21);
        a21.setLeftNeighbor(a22);
        a22.setLeftNeighbor(a23);
        a23.setLeftNeighbor(a24);
        a25.setLeftNeighbor(a26);
        a26.setLeftNeighbor(a27);
        a27.setLeftNeighbor(a28);
        a28.setLeftNeighbor(a29);
        a29.setLeftNeighbor(a30);
        a30.setLeftNeighbor(a31);
        a31.setLeftNeighbor(a32);

        a2.setRightNeighbor(a1);
        a3.setRightNeighbor(a2);
        a4.setRightNeighbor(a3);
        a5.setRightNeighbor(a4);
        a6.setRightNeighbor(a5);
        a7.setRightNeighbor(a6);
        a8.setRightNeighbor(a7);
        a9.setRightNeighbor(a8);
        a11.setRightNeighbor(a10);
        a12.setRightNeighbor(a11);
        a13.setRightNeighbor(a12);
        a14.setRightNeighbor(a13);
        a15.setRightNeighbor(a14);
        a17.setRightNeighbor(a16);
        a18.setRightNeighbor(a17);
        a19.setRightNeighbor(a18);
        a20.setRightNeighbor(a19);
        a21.setRightNeighbor(a20);
        a22.setRightNeighbor(a21);
        a23.setRightNeighbor(a22);
        a24.setRightNeighbor(a23);
        a26.setRightNeighbor(a25);
        a27.setRightNeighbor(a26);
        a28.setRightNeighbor(a27);
        a29.setRightNeighbor(a28);
        a30.setRightNeighbor(a29);
        a31.setRightNeighbor(a30);
        a32.setRightNeighbor(a31);

        a1.setFrontNeighbor(a32);
        a2.setFrontNeighbor(a31);
        a3.setFrontNeighbor(a30);
        a4.setFrontNeighbor(a29);
        a7.setFrontNeighbor(a12);
        a8.setFrontNeighbor(a11);
        a9.setFrontNeighbor(a10);
        a10.setFrontNeighbor(a9);
        a11.setFrontNeighbor(a8);
        a12.setFrontNeighbor(a7);
        a13.setFrontNeighbor(a18);
        a14.setFrontNeighbor(a17);
        a15.setFrontNeighbor(a16);
        a16.setFrontNeighbor(a15);
        a17.setFrontNeighbor(a14);
        a18.setFrontNeighbor(a13);
        a21.setFrontNeighbor(a28);
        a22.setFrontNeighbor(a27);
        a23.setFrontNeighbor(a26);
        a24.setFrontNeighbor(a25);
        a25.setFrontNeighbor(a24);
        a26.setFrontNeighbor(a23);
        a27.setFrontNeighbor(a22);
        a28.setFrontNeighbor(a21);
        a29.setFrontNeighbor(a4);
        a30.setFrontNeighbor(a3);
        a31.setFrontNeighbor(a2);
        a32.setFrontNeighbor(a1);

        return new Hospital(Arrays.asList(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
                a11, a12, a13, a14, a15, a16, a17, a18, a19, a20,
                a21, a22, a23, a24, a25, a26, a27, a28, a29, a30,
                a31, a32));
    }

    public static Hospital step2(Hospital hospital) {

        hospital.incrementTime(Constantes.NEXT_TIME_STEP);

        for(Room room : hospital.getRooms()) {

            //Interventions des infirmières qui résouds les problèmes et réinitialisé certaines chambres
            if(Arrays.asList(2, 6, 23, 26, 31).contains(room.getId())) {
                resetRoomDevices(room);
            }

            //Interventions d'une infirmière qui a débranché la machine de la chambre 15
            if(room.getId() == 15) {
                List<Device> newDevices = new ArrayList<Device>();
                for(Device device : room.getDevices()) {
                    if(device.getEndOfProgram() < 60) {
                        //do nothing : on l'enlève de la liste
                    } else {
                        newDevices.add(device);
                    }
                }
                room.setDevices(newDevices);
                room.setTau(0);
            }
        }
        return hospital;
    }

    public static Hospital step3(Hospital hospital) {

        hospital.incrementTime(Constantes.NEXT_TIME_STEP);

        for(Room room : hospital.getRooms()) {

            //Interventions des infirmières qui résouds les problèmes et réinitialisé certaines chambres
            if(Arrays.asList(9, 10, 27).contains(room.getId())) {
                resetRoomDevices(room);
            }

            //L'infirmière a rebranché une machine en chambre 15
            if(room.getId() == 15) {
                Device newDevice = new Device(151, Constantes.INFINITY, false);
                List<Device> newListDevices = room.getDevices();
                newListDevices.add(newDevice);
                room.setDevices(newListDevices);
            }
        }
        return hospital;
    }

    public static Hospital step4(Hospital hospital) {
        //Tout vas bien, et les infirmières on rajouté des machines en salle 19 et 20
        hospital.incrementTime(Constantes.NEXT_TIME_STEP);

        for(Room room : hospital.getRooms()) {

            if(Arrays.asList(19, 20).contains(room.getId())) {
                Device d = new Device(Integer.parseInt(room.getId() + "1"), Constantes.INFINITY, false);
                room.setDevices(Arrays.asList(d));
            }
        }
        return hospital;
    }

    /***
     * Reset all devices of the room
     * @param room
     */
    private static void resetRoomDevices(Room room) {
        for(Device device : room.getDevices()) {
            if(device.isInCriticalState()) {
                device.setInCriticalState(false);
                device.setEndOfProgram(Constantes.INFINITY);
            }

            if(device.getEndOfProgram() < 60) {
                device.setEndOfProgram(Constantes.INFINITY);
            }
        }
        room.setTau(0);
    }
}
