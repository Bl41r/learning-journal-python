# tests.py
import pytest

from pyramid import testing


def test_detail():
    from .views.default import detail
    request = testing.DummyRequest()
    request.matchdict = {'id': '12'}
    info = detail(request)
    assert "entry" in info


def test_new():
    from .views.default import new
    request = testing.DummyRequest()
    info = new(request)
    assert info == {}


def test_edit():
    from .views.default import edit
    request = testing.DummyRequest()
    request.matchdict = {'id': '12'}
    info = edit(request)
    assert info['entry']['title'] == 'Day12'


def test_home_page():
    from .views.default import home_page
    request = testing.DummyRequest()
    info = home_page(request)
    assert 'entries' in info

# ------- Functional Tests -------


@pytest.fixture()
def testapp():
    from website import main
    app = main({})
    from webtest import TestApp
    return TestApp(app)


def test_layout_root(testapp):
    response = testapp.get('/', status=200)
    assert b'Entries' in response.body


def test_root_contents(testapp):
    response = testapp.get('/', status=200)
    assert b'<td>' in response.body

