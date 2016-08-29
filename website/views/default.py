from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


import os

HERE = os.path.dirname(__file__)

ENTRIES_DATA = [
    {
        'title': 'Day12',
        'id': '12',
        'creation_date': 'August 23, 2016',
        'body': '<p>Today, we learned about templating with Jinja, and about the binary tree data type.  I spent most of the time revising old data structures, since it is not a good idea to coninue building upon something that is not perfect.  I also got my journal site deployed with the templates working.  Lastly, we formed project groups, and I will be working on my idea for a market analysis web application.</p>'
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
    """Grab entry based on id."""
    for entry in ENTRIES_DATA:
        if entry['id'] == id:
            return entry
    return 404


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_page(request):
    """Return all entries for the home route."""
    return {"entries": ENTRIES_DATA}


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail(request):
    """Send individual entry for detail view."""
    data = grab_entry_by_id(request.matchdict['id'])
    print(data)     # debugging
    if data != 404:
        return {"entry": data}
    # handle error somehow here


@view_config(route_name='edit', renderer='../templates/edit.jinja2')
def edit(request):
    """Send individual entry to be edited."""
    data = grab_entry_by_id(request.matchdict['id'])
    print(data)     # debugging
    if data != 404:
        return {"entry": data}


@view_config(route_name='new', renderer='../templates/new.jinja2')
def new(request):
    """Return empty dict for new entry."""
    return {}

#step 3 stuff
#@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
#def my_view(request):
#    print(request)  # debug
#    try:
#        query = request.dbsession.query(MyModel)
#        one = query.filter(MyModel.name == 'one').first()
#    except DBAPIError:
#        return Response(db_err_msg, content_type='text/plain', status=500)
#    return {'one': one, 'project': 'website'}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_website_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
