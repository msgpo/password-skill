Feature: login
    Scenario: user login english
        Given an English speaking user
        When the user says "login hallo"
        Then "password-skill" should reply with "welcome"
        Then mycroft should send the message "skillmanager.activate"
    Scenario: user login german
        Given an English speaking user
        When the user says "Login hallo"
        Then "password-skill" should reply with "Willkommen"
        Then mycroft should send the message "skillmanager.activate"
