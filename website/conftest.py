"""Testing fixtures."""
import pytest
import transaction
import os

from pyramid import testing

from .models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)

from .models.meta import Base
from .models.mymodel import MyModel

from passlib.apps import custom_app_context as pwd_context


TEST_SETTINGS = {'sqlalchemy.url': 'postgres:///david'}
PASSWORD = 'secret password'
ENCRYPTED_PASSWORD = pwd_context.encrypt(PASSWORD)

# Thanks to David Banks for helping set up a few of these fixtures


@pytest.fixture(scope="function")
def populated_db(request, sqlengine):
    session_factory = get_session_factory(sqlengine)
    dbsession = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:
        entry = MyModel(title='title: Day 1', body='blah', creation_date='1999')
        dbsession.add(entry)

    def teardown():
        with transaction.manager:
            dbsession.query(MyModel).delete()

    request.addfinalizer(teardown)


@pytest.fixture(scope='function')
def auth_env():
    username = 'david'
    os.environ['AUTH_USER_LJ'] = username
    os.environ['AUTH_PASS_LJ'] = ENCRYPTED_PASSWORD

    return username, PASSWORD


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings=TEST_SETTINGS)
    config.include(".models")
    config.testing_securitypolicy(userid='david', permissive=True)
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def test_app():
    from website import main
    from webtest.app import TestApp

    app = main({}, **TEST_SETTINGS)
    return TestApp(app)
