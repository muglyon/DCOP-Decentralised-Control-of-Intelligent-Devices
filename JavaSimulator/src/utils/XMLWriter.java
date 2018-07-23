package utils;

import core.Hospital;
import core.Room;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;

/***
 * Ecriture du problem au format xml frodo JaCoP
 */
public class XMLWriter {

    private org.w3c.dom.Document doc;

    /***
     * Create and write the problemFile based on the current hospital environment to be used by Frodo
     * @param hospital
     */
    public void writeFileFor(Hospital hospital) {

        try {

            DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

            //Instance element
            doc = docBuilder.newDocument();
            org.w3c.dom.Element rootElement = doc.createElement("instance");
            doc.appendChild(rootElement);

            //Presentation element
            org.w3c.dom.Element presentation = doc.createElement("presentation");
            rootElement.appendChild(presentation);
            presentation.setAttribute("name", "MedicalProject");
            presentation.setAttribute("maxConstraintArity", "2");
            presentation.setAttribute("maximize", "false");
            presentation.setAttribute("format", "XCSP 2.1_FRODO");

            //Domains elements
            org.w3c.dom.Element domains = doc.createElement("domains");
            org.w3c.dom.Element domain = doc.createElement("domain");
            domain.setAttribute("name","time");
            domain.setAttribute("nbValues","10");
            domain.appendChild(doc.createTextNode("0 5 10 15 20 25 30 35 40 45 50 55 60 120 180 210 235 241"));
            domains.appendChild(domain);
            rootElement.appendChild(domains);

            //Agents et Variables elements
            org.w3c.dom.Element agents = doc.createElement("agents");
            org.w3c.dom.Element variables = doc.createElement("variables");

            for(Room room : hospital.getRooms()) {
                org.w3c.dom.Element agent = doc.createElement("agent");
                agent.setAttribute("name", "a" + room.getId());
                agents.appendChild(agent);

                org.w3c.dom.Element variable = doc.createElement("variable");
                variable.setAttribute("name", "v" + room.getId());
                variable.setAttribute("domain", "time");
                variable.setAttribute("agent", "a" + room.getId());
                variables.appendChild(variable);
            }

            rootElement.appendChild(agents);
            rootElement.appendChild(variables);

            //Predicates elements
            org.w3c.dom.Element predicates = doc.createElement("predicates");

            //A
            org.w3c.dom.Element predicate = doc.createElement("predicate");
            org.w3c.dom.Element parameters = doc.createElement("parameters");
            org.w3c.dom.Element expression = doc.createElement("expression");
            org.w3c.dom.Element functional = doc.createElement("functional");
            predicate.setAttribute("name", "contrainteA");
            parameters.appendChild(doc.createTextNode("int vi"));
            functional.appendChild(doc.createTextNode("gt(vi, 240)"));
            expression.appendChild(functional);
            predicate.appendChild(parameters);
            predicate.appendChild(expression);
            predicates.appendChild(predicate);

            //B1 : si la machine est en état critique
            predicate = doc.createElement("predicate");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            predicate.setAttribute("name", "contrainteB1");
            parameters.appendChild(doc.createTextNode("int vi"));
            functional.appendChild(doc.createTextNode("lt(vi, 10)"));
            expression.appendChild(functional);
            predicate.appendChild(parameters);
            predicate.appendChild(expression);
            predicates.appendChild(predicate);

            //D et E
            predicate = doc.createElement("predicate");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            predicate.setAttribute("name", "contrainteDouE");
            parameters.appendChild(doc.createTextNode("int vi"));
            functional.appendChild(doc.createTextNode("lt(vi, 30)"));
            expression.appendChild(functional);
            predicate.appendChild(parameters);
            predicate.appendChild(expression);
            predicates.appendChild(predicate);

            rootElement.appendChild(predicates);

            //Functions elements
            org.w3c.dom.Element functions = doc.createElement("functions");

            //B2 : si la machine n'est pas en état critique
            org.w3c.dom.Element function = doc.createElement("function");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            function.setAttribute("name", "contrainteB2");
            parameters.appendChild(doc.createTextNode("int vi int etatProgML"));
            functional.appendChild(doc.createTextNode("le(vi, etatProgML)"));
            expression.appendChild(functional);
            function.appendChild(parameters);
            function.appendChild(expression);
            functions.appendChild(function);

            //C : voisinage
            function = doc.createElement("function");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            function.setAttribute("name", "contrainteC");
            parameters.appendChild(doc.createTextNode("int vi int vj"));
            functional.appendChild(doc.createTextNode("or(eq(abs(sub(vi,vj)), 0), gt(abs(sub(vi,vj)), 30))"));
            expression.appendChild(functional);
            function.appendChild(parameters);
            function.appendChild(expression);
            functions.appendChild(function);

            //F : RAS
            function = doc.createElement("function");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            function.setAttribute("name", "contrainteF");
            parameters.appendChild(doc.createTextNode("int vi"));
            functional.appendChild(doc.createTextNode("ge(vi, 240)"));
            expression.appendChild(functional);
            function.appendChild(parameters);
            function.appendChild(expression);
            functions.appendChild(function);

            //Priorité
            function = doc.createElement("function");
            parameters = doc.createElement("parameters");
            expression = doc.createElement("expression");
            functional = doc.createElement("functional");
            function.setAttribute("name", "priority");
            parameters.appendChild(doc.createTextNode("int vi int vj"));
            functional.appendChild(doc.createTextNode("gt(vi, vj)"));
            expression.appendChild(functional);
            function.appendChild(parameters);
            function.appendChild(expression);
            functions.appendChild(function);

            rootElement.appendChild(functions);

            //Constraints elements
            org.w3c.dom.Element constraints = doc.createElement("constraints");

            for(Room room : hospital.getRooms()) {

                boolean hasEmergency = room.hasEmergency();
                int endingTime = -1;

                if(room.hasNoDevices()) {
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_have_0_device",
                            "v" + room.getId(),
                            "1",
                            "contrainteA",
                            "v" + room.getId()
                    ));
                }

                if(hasEmergency){
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_have_emergency",
                            "v" + room.getId(),
                            "1",
                            "contrainteB1",
                            "v" + room.getId()
                    ));

                } else {

                     endingTime = room.getTimeWhenFirstDeviceWillEnd();

                    if(endingTime <= 30 && endingTime != -1) {
                        constraints.appendChild(getXMLContraint(
                                "a" + room.getId() + "_prog_end_in_" + endingTime,
                                "v" + room.getId(),
                                "2",
                                "contrainteB2",
                                "v" + room.getId() + " " + endingTime
                        ));
                    }
                }

                Room neighbor = room.getFrontNeighbor();
                if(neighbor != null && neighbor.getId() > room.getId()) { //comparaison des Ids pour éviter les doublons
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_a" + neighbor.getId() + "_neighbors",
                            "v" + room.getId() + " v" + neighbor.getId(),
                            "2",
                            "contrainteC",
                            "v" + room.getId() + " v" + neighbor.getId()
                    ));
                }

                neighbor = room.getLeftNeighbor();
                if(neighbor != null && neighbor.getId() > room.getId()) { //comparaison des Ids pour éviter les doublons
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_a" + neighbor.getId() + "_neighbors",
                            "v" + room.getId() + " v" + neighbor.getId(),
                            "2",
                            "contrainteC",
                            "v" + room.getId() + " v" + neighbor.getId()
                    ));
                }

                neighbor = room.getRightNeighbor();
                if(neighbor != null && neighbor.getId() > room.getId()) { //comparaison des Ids pour éviter les doublons
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_a" + neighbor.getId() + "_neighbors",
                            "v" + room.getId() + " v" + neighbor.getId(),
                            "2",
                            "contrainteC",
                            "v" + room.getId() + " v" + neighbor.getId()
                    ));
                }

                if(room.isTauToBig()) {
                    constraints.appendChild(getXMLContraint(
                            "tau" + room.getId() + "_" + room.getTau(),
                            "v" + room.getId(),
                            "1",
                            "contrainteDouE",
                            "v" + room.getId()
                    ));
                }

                if(!hasEmergency && endingTime > 30 && room.getTau() < 180) {
                    constraints.appendChild(getXMLContraint(
                            "a" + room.getId() + "_RAS",
                            "v" + room.getId(),
                            "1",
                            "contrainteF",
                            "v" + room.getId()
                    ));
                }

//                if(!hasEmergency && !room.hasNoDevices() && (endingTime < 30 || /*room.getTau() > 180*/room.isTauToBig())){
//                    for (Room r : hospital.getRooms()) {
//
//                        if (r.needIntervention()
//                                && r.getId() != room.getId()
//                                && room.getPriority() < r.getPriority()
//                                && !room.hasForNeighboor(r)) {
//
//                            constraints.appendChild(getXMLContraint(
//                                    "a" + room.getId() + "_less_priority_then_a" + r.getId(),
//                                    "v" + room.getId() + " v" + r.getId(),
//                                    "2",
//                                    "priority",
//                                    "v" + room.getId() + " v" + r.getId()
//                            ));
//                        }
//                    }
//                }
            }
            rootElement.appendChild(constraints);

            //write the content into xml file
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();

            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");

            transformer.transform(new DOMSource(doc), new StreamResult(new File(Constantes.PROBLEM_XML_FILE)));
            System.out.println("Successfully write the xml problem file !");

        }catch(ParserConfigurationException pce){
            pce.printStackTrace();
        }catch(TransformerException tfe){
            tfe.printStackTrace();
        }
    }

    private Element getXMLContraint(String name, String scope, String arity, String ref, String values) {
        Element constraint = doc.createElement("constraint");
        Element c_param = doc.createElement("parameters");
        constraint.setAttribute("name", name);
        constraint.setAttribute("scope", scope);
        constraint.setAttribute("arity", arity);
        constraint.setAttribute("reference", ref);
        c_param.appendChild(doc.createTextNode(values));
        constraint.appendChild(c_param);
        return constraint;
    }
}
