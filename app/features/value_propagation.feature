Feature: VALUE propagation behavior

	Scenario: Value selection
		Given an IA agent
		When get VALUE from parent after UTIL propagation
		Then should select the optimal assignment

	Scenario: Wrong format value
		Given an IA agent
		When parent send values to wrong format
		Then should raise an exception

	Scenario: Wrong matrix value
		Given an IA agent
		When matrix is Null
		Then should raise an exception

	Scenario: 1D matrix
		Given an IA agent
		When matrix has 1 dimension
		Then should return the min value index
		