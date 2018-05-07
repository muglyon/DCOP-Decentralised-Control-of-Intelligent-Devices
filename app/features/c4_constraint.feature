Feature: (c4) Patient importance
	
	Scenario: Patient with many devices is more important
		Given an AI in syringe pump
		When the room contains more then 5 devices and last passage was more then 3 hours ago
		Then AI should call healthcare professionals in less then 30 minutes

	Scenario: Patient with less devices does not need lot of interventions
		Given an AI in syringe pump
		When the room contains less then 5 devices and last passage was more then 3 hours ago
		Then AI in syringe pump should not call healthcare professionals

	Scenario: Patient with less devices is less important
		Given an AI in syringe pump
		When the room contains less then 5 devices and last passage was more then 4 hours ago
		Then AI should call healthcare professionals in less then 30 minutes