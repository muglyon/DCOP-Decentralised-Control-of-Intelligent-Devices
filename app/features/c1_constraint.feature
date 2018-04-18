Feature: (c1) number of device constraints

	Scenario: No devices in the supervisor room
		Given an IA agent supervisor
		When no devices are connected to this agent
		Then agent should not call the nurse 

	Scenario: No devices in the room
		Given an IA agent
		When no devices are connected to this agent
		Then agent should not call the nurse 