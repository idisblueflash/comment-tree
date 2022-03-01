from behave import then
from hamcrest import *

from app.models import User
from features.steps.utils import table_to_list


@then("we've got users as below")
def assert_users_in_db(context):
    payload = table_to_list(context.table)[0]
    with context.app.app_context():
        user = User.query.filter_by(username=payload['username']).first()
        assert_that(user.to_json(), has_entry('username', payload['username']))


@then('I got error message')
def assert_error_message(context):
    message = context.response.json['message']
    assert_that(message, has_items())


