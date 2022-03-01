from behave import fixture, use_fixture

from app import create_app, db


@fixture
def comment_tree_client(context, *args, **kwargs):
    app = create_app('behave')
    context.db = db
    context.app = app
    context.client = app.test_client()

    with app.app_context():
        db.create_all()

    yield context.client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def before_feature(context, feature):
    use_fixture(comment_tree_client, context)


def after_scenario(context, scenario):
    with context.client.session_transaction() as session:
        session.clear()
