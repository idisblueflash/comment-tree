Feature: As a user, I want to list/add comment then I can leave messages

  Scenario: Post the first Comment
    Given we've got an user "Cameron"
    And no comments exist
    When user post "/api/v1/comments/post/" with payload
      | message      | int(user_id) | timestamp           |
      | a new notice | 1            | 2020-11-02 10:00:00 |
    Then status code is 200
    When user get "/api/v1/comments/"
    Then status code is 200
    And I can get response as below
      | int(id) | message      | int(depth) | int(user_id) | timestamp           |
      | 1       | root message | 0          | 1            | 2020-11-02 10:00:00 |
      | 2       | a new notice | 1          | 1            | 2020-11-02 10:00:00 |

  Scenario: Post another Comment, reply root message
    Given we've got an user "Olivia123"
    When user post "/api/v1/comments/post/" with payload
      | message        | int(user_id) | timestamp          | left_index |
      | another notice | 2            | 2020-11-04 8:00:00 | 1          |
    Then status code is 200
    When user get "/api/v1/comments/"
    Then status code is 200
    And I can get response as below
      | int(id) | message        | int(depth) | int(user_id) | timestamp           |
      | 1       | root message   | 0          | 1            | 2020-11-02 10:00:00 |
      | 3       | another notice | 1          | 2            | 2020-11-04 8:00:00  |
      | 2       | a new notice   | 1          | 1            | 2020-11-02 10:00:00 |

  Scenario: Reply a Comment
    Given we've got an user "vemend456"
    When user post "/api/v1/comments/post/" with payload
      | message            | int(user_id) | timestamp           | left_index |
      | re: another notice | 3            | 2020-11-06 12:00:00 | 2          |
    Then status code is 200
    When user get "/api/v1/comments/"
    Then status code is 200
    And I can get response as below
      | int(id) | message            | int(depth) | int(user_id) | timestamp           |
      | 1       | root message       | 0          | 1            | 2020-11-02 10:00:00 |
      | 3       | another notice     | 1          | 2            | 2020-11-04 8:00:00  |
      | 4       | re: another notice | 2          | 3            | 2020-11-06 12:00:00 |
      | 2       | a new notice       | 1          | 1            | 2020-11-02 10:00:00 |

  Scenario: Reply a Comment when not login
    When user post "/api/v1/comments/post/" with payload
      | message            | int(user_id) | timestamp           | left_index |
      | re: another notice | 3            | 2020-11-06 12:00:00 | 2          |
    Then status code is 302
