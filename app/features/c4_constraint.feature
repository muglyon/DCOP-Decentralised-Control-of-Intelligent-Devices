Feature: (c4) Patient importance
	
	Scenario: Patient with many devices is more important
		Given an AI agent
		When the room contains more then 5 devices and last passage was more then 3 hours ago
		Then agent should call the nurse in less then 30 minutes

	Scenario: Patient with less devices does not need lot of interventions
		Given an AI agent
		When the room contains less then 5 devices and last passage was more then 3 hours ago
		Then agent should not call the nurse

	Scenario: Patient with less devices is less important
		Given an AI agent
		When the room contains less then 5 devices and last passage was more then 4 hours ago
		Then agent should call the nurse in less then 30 minutes