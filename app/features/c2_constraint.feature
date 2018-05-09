Feature: (c2) intervention depends on devices states

	Scenario: Device end its program soon
		Given an AI in syringe pump
		When an IoT device is ending its program in less then 30 minutes
		Then AI in syringe pump should call healthcare professionals before the end of its program

	Scenario: Device is in critical state
		Given an AI in syringe pump
		When an IoT device is in critical state and ends its program in less then 30 minutes
		Then AI in syringe pump should call healthcare professionals right now