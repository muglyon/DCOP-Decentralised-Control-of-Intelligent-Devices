Feature: MQTT Communications behavior

	Scenario: Wrong messages during DFS Generation
		Given an AI agent
		When receive UTIL message in DFS Generation
		Then should ignore the message

	Scenario: Wrong messages during UTIL Propagation
		Given an AI agent
		When receive VALUE message in UTIL Propagation
		Then should ignore the message

	Scenario: UTIL timeout
		Given an AI agent
		When child does not send UTIL message before TIMEOUT
		Then agent should proceed to value propagation

	Scenario: VALUE timeout
		Given an AI agent
		When parent does not send VALUE message before TIMEOUT
		Then agent should proceed anyway