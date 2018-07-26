package frodo_simulations;

import core.Hospital;
import utils.Constantes;

/***
 * Run Frodo DCOP (DPOP) algorithm in a random environment
 */
public class RandomSimulation {

    public static void main(String[] args) {
        Hospital hospital = new Hospital(Constantes.NB_AGENTS);

        hospital.setEveryRoomToCritical();
        Simulation.resolveDCOP(hospital);
    }
}
