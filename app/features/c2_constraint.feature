Feature: (c2) intervention depends on devices states

	Scenario: Device end its program soon
		Given an AI agent
		When a device is ending its program in less then 30 minutes
		Then agent should call the nurse before the end of its program

	Scenario: Device is in critical state
		Given an AI agent
		When device is in critical state and ends its program in less then 30 minutes
		Then agent should call the nurse right now