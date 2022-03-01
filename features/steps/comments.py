from behave import given, then
from hamcrest import assert_that, has_entries, equal_to

from app.models import Comment
from features.steps.utils import table_to_list


@given("existing comments below")
def assert_users_in_db(context):
    with context.app.app_context():
        for row in table_to_list(context.table):
            comment = Comment(**row)
            context.db.session.add(comment)
            context.db.session.commit()


@then("I can get response as below")
def assert_response_with_table(context):
    expect = table_to_list(context.table)
    real = context.response.json['comments']
    for index, item in enumerate(real):
        assert_that(item, has_entries(expect[index]))


@given("no comments exist")
def assert_empty_comments(context):
    with context.app.app_context():
        assert_that(len(Comment.query.all()), equal_to(0))
