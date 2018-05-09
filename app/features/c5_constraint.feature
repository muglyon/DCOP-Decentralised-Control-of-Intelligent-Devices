Feature: (c5) RAS constraint

	Scenario: Nothing to report
		Given an AI in syringe pump
		When there is nothing to report
		Then AI in syringe pump should not call healthcare professionals