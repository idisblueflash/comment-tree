Feature: As a user, I want to sign up then I can post comment

  Scenario: Sign up successfully
    When user post "/api/v1/sign-up/" with payload
      | username | password          | email           |
      | flash    | Flash&password123 | flash@email.com |
    Then status code is 200
    And we've got users as below
      | username | password          | email           |
      | flash    | Flash&password123 | flash@email.com |

  Scenario:  Sign up failed with hints
    When user post "/api/v1/sign-up/" with payload
      | username | password         | email             |
      | trinity  | trinity-password | trinity@email.com |
    Then status code is 400
    And I got error with "bad request"
    And I got error message

  Scenario: Sign up failed with existing username
    Given we've got an user "jerry"
    When user post "/api/v1/sign-up/" with payload
      | username | password          | email               |
      | jerry    | Jerry&password123 | jerry-new@email.com |
    Then status code is 400
    And I got error with "bad request"
    And I got error message

  Scenario: Sign up failed with existing username
    Given we've got an user "thomson"
    When user post "/api/v1/sign-up/" with payload
      | username   | password            | email             |
      | thomson123 | Thomson&password123 | thomson@email.com |
    Then status code is 400
    And I got error with "bad request"
    And I got error message
