Feature: (c3) neighborhood constraint
	
	Scenario: Neighbors synchronized
		Given two AI in syringe pump in two separate rooms next to each other
		When both AI call healthcare professionals in almost the same time t1 and t2 with t1 > t2
		Then AI in syringe pump should call healthcare professionals together synchronized in t2

	Scenario: Neighbors not synchronized
		Given two AI in syringe pump in two separate rooms next to each other
		When one is calling healthcare professionals but not the other one
		Then only the AI who need intervention should call healthcare professionals