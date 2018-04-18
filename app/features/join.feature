Feature: JOIN operator behavior

	Scenario: Increase dimensions
		Given two matrix
		When they have the same dimensions
		Then join operation should return matrix with dimension + 1

	Scenario: Different dimensions
		Given two matrix
		When they do not have the same dimensions
		Then join operation should return matrix with biggest matrix dimension + 1

	Scenario: Values in the joined matrix
		Given two matrix
		When they have the same dimensions
		Then each joined matrix value is the sum of the corresponding cells in the two source matrices 

	Scenario: Null matrix
		Given two matrix
		When one of them is Null
		Then join operation should return the other matrix (or raise an exception if both are Null)