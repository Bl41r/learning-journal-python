# tests.py
import pytest

from pyramid import testing


def test_detail_view():
    from .views.default import detail
    request = testing.DummyRequest()
    request.matchdict = {'id': '12'}
    info = detail(request)
    assert "entry" in info

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
