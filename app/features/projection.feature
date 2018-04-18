Feature: PROJECTION behavior

	Scenario: Reduction of dimensions
		Given a matrix
		When project the agent
		Then result is a matrix has one less dimension

	Scenario: Result values
		Given a matrix
		When project the agent
		Then result contain optimal utility for agent value chosen