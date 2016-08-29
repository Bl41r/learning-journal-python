import pytest
import transaction

from pyramid import testing

from .models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from .models.meta import Base

from .models.mymodel import MyModel


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")
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

def test_model_gets_added(new_session):
    assert len(new_session.query(MyModel).all()) == 0
    model = MyModel(title="TestDay", body='blah..', creation_date='A long time ago..')
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(MyModel).all()) == 1

#def test_detail():
#    from .views.default import detail
#    request = testing.DummyRequest()
#    request.matchdict = {'id': '1'}
#    info = detail(request)
#    assert "entry" in info


#def test_new():
#    from .views.default import new
#    request = testing.DummyRequest()
#    info = new(request)
#    assert 'entry' in info


#def test_edit():
#    from .views.default import edit
#    request = testing.DummyRequest()
#    request.matchdict = {'id': '1'}
#    info = edit(request)
#    #assert info['entry']['title'] == 'Day12'
#    print(info)
#    assert 1 == 2


#def test_home_page():
#    from .views.default import my_view
#    request = testing.DummyRequest()
#    info = my_view(request)
#    assert 'entries' in info

## ------- Functional Tests -------1


#@pytest.fixture()
#def testapp():
#    from website import main
#    app = main({})
#    from webtest import TestApp
#    return TestApp(app)


#def test_layout_root(testapp):
#    response = testapp.get('/', status=200)
#    assert b'Entries' in response.body


#def test_root_contents(testapp):
#    response = testapp.get('/', status=200)
#    assert b'<table id="entries_table">' in response.body


#def test_new_layout(testapp):
#    response = testapp.get('/journal/new-entry', status=200)
#    assert b'Make a New Entry' in response.body


#def test_detail_page(testapp):
#    response = testapp.get('/journal/12', status=200)
#    assert b'<h3>Day12 - August 23, 2016</h3>' in response.body


#def test_edit_page(testapp):
#    response = testapp.get('/journal/12/edit-entry')
#    assert b'<h1>Edit an Existing Entry</h1>' in response.body
