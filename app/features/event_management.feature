Feature: Events Management
  Specific behaviors when an event happened in the hospital outside of the system

  Scenario: Event Manager monitoring a room and send urgent message to server if needed
    Given an AI in syringe pump
    And the event manager
    When a device of the room enter into a critical state
    Then AI in syringe pump should send urgent message to server

  Scenario: Event Manager monitoring a room and send urgent message to server if needed (2)
    Given an AI in syringe pump
    And the event manager
    When a device enter into a critical state during calculation
    Then AI in syringe pump should send urgent message to server

  Scenario: Server send "ON" messages with specific root on urgent demands
    Given a server interacting with AI agents in syringe pump
    When receive an 'URGT' message from AI in syringe pump
    Then server should send 'ON' messages to every AI in syringe pump
    And should choose the sender of the 'URGT' message as root