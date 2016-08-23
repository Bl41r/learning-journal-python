from pyramid.view import view_config
import os

HERE = os.path.dirname(__file__)
ENTRIES = [
    {
        "title": "This is number 1",
        "id": 1,
        "date": "August 23"
        "body": "blah blah"
    },
    {
        "title": "This is number 2",
        "id": 2,
        "date": "August 24"
        "body": "blah blah"
    },
]

@view_config(route_name='home', renderer='templates/detail.jinja2')
def home_page(request):
    imported_text = open(os.path.join(HERE, 'templates/index.html')).read()
    return imported_text


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail(request):
    imported_text = open(os.path.join(HERE, 'templates/detail.html')).read()
    return imported_text


@view_config(route_name='edit', renderer='templates/detail.jinja2')
def edit(request):
    imported_text = open(os.path.join(HERE, 'templates/edit.html')).read()
    return imported_text


@view_config(route_name='new', renderer='templates/detail.jinja2')
def new(request):
    imported_text = open(os.path.join(HERE, 'templates/new.html')).read()
    return imported_text
