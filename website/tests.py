import pytest
from pyramid import testing


def test_detail_view_has_title():
    from .views import test_detail_view_has_title

    request = testing.DummyRequest()
    info = detail(request)
    assert "title" in info.keys()


@pytest.fixture()
def testapp():
    from website import main
    app = main({})
    from webtest import testapp
    return TestApp(app)


def test_layout_route(testapp):
    response = testapp.get('/', status=200)
    assert b'Footer Line Here' in response.body
