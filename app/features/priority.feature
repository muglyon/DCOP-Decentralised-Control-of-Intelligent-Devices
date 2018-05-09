Feature: Priority constraint

  Scenario: an AI agent calls healthcare Professional two iterations in a row
    Given a server interacting with AI agents in syringe pump
    When an AI agent with priority 0 needs intervention in less then 30 minutes in two iterations in a row
    Then server should increase priority of this room

  Scenario: an AI agent was calling healthcare Professional but not does not
    Given a server interacting with AI agents in syringe pump
    When an AI agent with priority 5 does not need intervention anymore
    Then AI agent priority should be 0