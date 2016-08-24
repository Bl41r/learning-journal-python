from pyramid.view import view_config
import os

HERE = os.path.dirname(__file__)

ENTRIES_DATA = [
    {
        'title': 'Day12',
        'id': '12',
        'creation_date': 'August 23, 2016',
        'body': '<p>Today, we...</p>'
    },
    {
        'title': 'Day11',
        'id': '11',
        'creation_date': 'August 22, 2016',
        'body': '<p>Today, we code reviewed our server-from-scratch code.  We then learned about Pyramid and worked on this very site.  We also built the deque data structure, and worked on more testing and revising for previous structures.</p>'
    },
    {
        'title': 'Day10',
        'id': '10',
        'creation_date': 'August 21, 2016',
        'body': '<p>asdf</p>'
    },
    {
        'title': 'Day9',
        'id': '9',
        'creation_date': 'August 20, 2016',
        'body': '<p>asdf</p>'
    },
    {
        'title': 'Day8',
        'id': '8',
        'creation_date': 'August 19, 2016',
        'body': '<p>asdf</p>'
    },
]

# sort the data based on the id maybe needed here


def grab_entry_by_id(id):
    for entry in ENTRIES_DATA:
        if entry['id'] == id:
            return entry
    return 404


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_page(request):
    return {"entries": ENTRIES_DATA}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail(request):
    data = grab_entry_by_id(request.matchdict['id'])
    print(data)
    if data != 404:
        return {"entry": data}
    # handle error somehow here


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit(request):
    return {"entries": ENTRIES_DATA}


@view_config(route_name='new', renderer='templates/new.jinja2')
def new(request):
    return {"entries": ENTRIES_DATA}
