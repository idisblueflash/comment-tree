from time import time

from behave import given, when, then
from hamcrest import *

from app.api.constants import MONTH_SECONDS
from app.models import User
from flask import current_app

from features.steps.utils import table_to_list


@then('I should see the alert "{message}"')
def logged_in(context, message):
    data = context.page.data.decode()
    print(f'DEBUG: message={message}, data={data}')
    assert message in context.page.data.decode()


@given('we\'ve got an user "{username}"')
def set_user(context, username):
    user = User()
    user.username = username
    user.email = f'{username}@email.com'
    user.password = f'{username}-password'
    with context.app.app_context():
        context.db.session.add(user)
        context.db.session.commit()
        context.user = User.query.filter_by(username=username).first()


@when('user post "{api_path}" with payload')
def post_api(context, api_path):
    payload = table_to_list(context.table)[0]
    with context.app.app_context():
        current_app.logger.info(f'payload={payload}, api path={api_path}')

    with context.client.session_transaction() as session:
        if 'user' in context:
            session['_user_id'] = context.user.id
            session['username'] = context.user.username

    context.response = context.client.post(api_path, json=payload)


@when('user get "{api_path}"')
def get_api(context, api_path):
    with context.app.app_context():
        current_app.logger.info(f'api path={api_path}')

    context.response = context.client.get(api_path)


@then("status code is {status_code}")
def assert_status_code(context, status_code):
    status_code = int(status_code)
    with context.app.app_context():
        context.app.logger.info(f'context.response.json={context.response.json}')
    with context.client.session_transaction() as session:
        context.app.logger.info(f'session user_id={session.get("_user_id")}')
    assert_that(context.response.status_code, equal_to(status_code))


@then('I got error with "{error_name}"')
def assert_error_message(context, error_name):
    assert_that(context.response.json['error'], equal_to(error_name))


@then("expiration is within {month} month")
def assert_expiration_within_months(context, month):
    real_duration = context.response.json['exp'] - int(time())
    expected_duration = int(month) * MONTH_SECONDS
    assert_that(real_duration, equal_to(expected_duration))


@then("I can get {response_key} in response")
def assert_response_exist_with_key(context, response_key):
    with context.app.app_context():
        current_app.logger.info(f'response={context.response.json}')

    assert_that(context.response.json.get(response_key), not_none())


@then("I can get user_id in session")
def assert_user_id_in_session(context):
    with context.client.session_transaction() as session:
        assert_that(session.get('_user_id'), not_none())


@then("I can not get user_id in session")
def assert_no_user_id_in_session(context):
    with context.client.session_transaction() as session:
        assert_that(session.get('_user_id'), none())
