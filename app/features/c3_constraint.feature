Feature: (c3) neighborhood constraint
	
	Scenario: Neighbors synchronized
		Given two neighbors IA agents
		When they call the nurse in almost the same time t1 and t2 with t1 > t2
		Then agents should call the nurse together synchronized in t2

	Scenario: Neighbors not synchronized
		Given two neighbors IA agents
		When one is calling the nurse but not the other one
		Then agents should not be synchronized	