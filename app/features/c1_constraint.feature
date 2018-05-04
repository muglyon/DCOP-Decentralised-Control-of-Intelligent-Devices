Feature: (c1) number of device constraints

	Scenario: No devices in the supervisor room
		Given an AI agent supervisor
		When no devices are connected to this agent
		Then agent should not call health workers

	Scenario: No devices in the room
		Given an AI agent
		When no devices are connected to this agent
		Then agent should not call health workers