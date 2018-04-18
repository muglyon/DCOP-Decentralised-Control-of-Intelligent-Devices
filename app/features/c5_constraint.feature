Feature: (c5) RAS constraint

	Scenario: Nothing to report
		Given an IA agent
		When there is nothing to report
		Then agent should not call the nurse