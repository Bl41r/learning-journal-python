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
    """Test that a new model gets added."""
    assert len(new_session.query(MyModel).all()) == 0
    model = MyModel(title="TestDay", body='blah..', creation_date='A long time ago in a galaxy far, far away....')
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(MyModel).all()) == 1


def dummy_http_request(new_session, method='GET'):
    """Create the testing request and attach dbsession."""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = new_session
    return request


def test_my_view(new_session):
    """Test main home page that entries is retrieved."""
    from .views.default import my_view

    new_session.add(MyModel(title="test", body='blah..', creation_date='1066 AD'))
    new_session.flush()

    http_request = dummy_http_request(new_session)
    result = my_view(http_request)
    assert 'entries' in result


def test_new_get(new_session):
    """Test new entry get req."""
    from .views.default import new

    new_session.add(MyModel(title="test", body='blah..', creation_date='1066 AD'))
    new_session.flush()

    http_request = dummy_http_request(new_session)
    result = new(http_request)
    assert result['entry']['goofed'] == 0


def test_new_submit_fail(new_session):
    """Test new entry fails when data incomplete."""
    from .views.default import new

    new_session.add(MyModel(title='', body='this should fail', creation_date=''))
    new_session.flush()

    http_request = dummy_http_request(new_session, 'POST')
    http_request.POST['title'] = ''
    http_request.POST['body'] = 'this should fail'
    http_request.POST['creation_date'] = ''
    result = new(http_request)
    assert result['entry']['goofed'] == 1


def test_detail(new_session):
    """Test the correct entry is retrieved in detail view."""
    from .views.default import detail

    new_session.add(MyModel(title="test", body='blah..', creation_date='1066 AD'))
    new_session.flush()

    http_request = dummy_http_request(new_session)
    http_request.matchdict['id'] = 1
    result = detail(http_request)
    assert getattr(result['entry'], 'title') == 'test'


def test_edit(new_session):
    """Test the editing page."""
    from .views.default import edit

    new_session.add(MyModel(title="test", body='blah..', creation_date='1066 AD'))
    new_session.flush()

    http_request = dummy_http_request(new_session, 'POST')
    http_request.matchdict['id'] = 1
    http_request.POST['title'] = 'new title'
    http_request.POST['body'] = 'blah 2.0'
    http_request.POST['creation_date'] = '1066 AD'
    result = edit(http_request)
    assert result['updated'] == True
