Feature: (c1) number of device constraints

	Scenario: No devices in the supervisor room
		Given an AI in syringe pump (supervisor)
		When no IoT devices are connected to the AI in syringe pump
		Then AI in syringe pump should not call healthcare professionals

	Scenario: No devices in the room
		Given an AI in syringe pump
		When no IoT devices are connected to the AI in syringe pump
		Then AI in syringe pump should not call healthcare professionals