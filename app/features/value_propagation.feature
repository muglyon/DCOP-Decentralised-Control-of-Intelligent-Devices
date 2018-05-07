Feature: VALUE propagation behavior

	Scenario: Value selection
		Given an AI in syringe pump
		When get VALUE from parent after UTIL propagation
		Then should select the optimal assignment

	Scenario: Wrong format value
		Given an AI in syringe pump
		When parent send values to wrong format
		Then should raise an exception

	Scenario: Wrong matrix value
		Given an AI in syringe pump
		When matrix is Null
		Then should raise an exception

	Scenario: 1D matrix
		Given an AI in syringe pump
		When matrix has 1 dimension
		Then should return the min value index
		