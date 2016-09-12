import pytest
import os
from pyramid import testing
from .models.mymodel import MyModel


def test_unauth_view(test_app, populated_db):
    response = test_app.get('/')
    assert response.status_code == 200


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
    assert result['updated'] is True
