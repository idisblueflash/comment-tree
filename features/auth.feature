Feature: As a website owner, I want to secure my website with Token

  Scenario: Get Token with Username and Password
    Given we've got an user "admin"
    When user post "/api/v1/get-token/" with payload
      | username | password       |
      | admin    | admin-password |
    Then status code is 200
    And I can get token in response
    And I can get username in response
    And I can get email in response

  Scenario: Get Token with un-registered Username and Password
    When user post "/api/v1/get-token/" with payload
      | username | password       |
      | tom      | admin-password |
    Then status code is 401

  Scenario: Get Token with wrong Password
    Given we've got an user "jerry"
    When user post "/api/v1/get-token/" with payload
      | username | password       |
      | jerry    | wrong-password |
    Then status code is 403
    And I got error with "forbidden"

  Scenario: Get Token with wrong Username
    Given we've got an user "mary"
    When user post "/api/v1/get-token/" with payload
      | username | password      |
      | jerry    | mary-password |
    Then status code is 403
    And I got error with "forbidden"

  Scenario: Get Token with Email and Password
    Given we've got an user "susan"
    When user post "/api/v1/get-token/" with payload
      | email           | password       |
      | susan@email.com | susan-password |
    Then status code is 200
    And I can get token in response

  Scenario: Get Token with Remember Me
    Given we've got an user "kite"
    When user post "/api/v1/get-token/" with payload
      | username | password      | remember |
      | kite     | kite-password | True     |
    Then status code is 200
    And I can get token in response
    And expiration is within 1 month

  Scenario: Logout when browser close(refresh homepage will logout)
    Given we've got an user "maggie"
    When user post "/api/v1/get-token/" with payload
      | username | password        | remember |
      | maggie   | maggie-password | False    |
    Then status code is 200
    And I can get user_id in session
    When user get "/"
    Then I can not get user_id in session

  Scenario: Keep Login on remember me
    Given we've got an user "sunny"
    When user post "/api/v1/get-token/" with payload
      | username | password       | remember |
      | sunny    | sunny-password | True     |
    Then status code is 200
    And I can get user_id in session
    When user get "/"
    Then I can get user_id in session
