Feature: (c3) neighborhood constraint
	
	Scenario: Neighbors synchronized
		Given two neighbors AI agents
		When they call health workers in almost the same time t1 and t2 with t1 > t2
		Then agents should call health workers together synchronized in t2

	Scenario: Neighbors not synchronized
		Given two neighbors AI agents
		When one is calling health workers but not the other one
		Then agents should not be synchronized	