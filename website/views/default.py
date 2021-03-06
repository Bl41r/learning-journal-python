from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import MyModel
import os
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..security import verify_user


HERE = os.path.dirname(__file__)

ENTRIES_DATA = [
    {
        'title': 'Day12',
        'creation_date': 'August 23, 2016',
        'body': 'Today, we learned about templating with Jinja, and about the binary tree data type.  I spent most of the time revising old data structures, since it is not a good idea to coninue building upon something that is not perfect.  I also got my journal site deployed with the templates working.  Lastly, we formed project groups, and I will be working on my idea for a market analysis web application.'
    },
]


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    if request.method == 'GET':
        return {'bogus_attempt': False}
    if request.method == 'POST':
        username = str(request.params.get('user', ''))
        password = str(request.params.get('pass', ''))
        print('user/pass:', username, password)

        if verify_user(username, password):
            print('User verfied.')
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {'bogus_attempt': True}


@view_config(route_name='logout', renderer='../templates/logout.jinja2')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail(request):
    """Send individual entry for detail view."""
    query = request.dbsession.query(MyModel)
    data = query.filter_by(id=request.matchdict['id']).first()
    return {"entry": data}


@view_config(route_name='edit', renderer='../templates/edit.jinja2', permission='root')
def edit(request):
    """Send individual entry to be edited."""
    query = request.dbsession.query(MyModel)
    data = query.filter_by(id=request.matchdict['id']).one()
    data2 = {'id': data.id, 'body': data.body, 'creation_date': data.creation_date, 'title': data.title}
    updated = False
    #   using data2 prevents data from being written to the db.  Use data
    #   to like data.body = req.... to change database (autocommit is on)
    if request.method == 'POST':
        updated = True
        data2['creation_date'] = request.POST['creation_date']
        data2['body'] = request.POST['body']
        data2['title'] = request.POST['title']

        #updating # comment out for testing
        data.body = data2['body']
        data.title = data2['title']
        data.creation_date = data2['creation_date']

    return {'entry': data2, 'updated': updated}


@view_config(route_name='new', renderer='../templates/new.jinja2', permission='root')
def new(request):
    """Return empty dict for new entry."""
    goofed = {'goofed': 0}
    if request.method == 'GET':
        return {'entry': goofed}
    if request.method == 'POST':
        new_model = MyModel(title=request.POST['title'], body=request.POST['body'], creation_date=request.POST['creation_date'])
        if new_model.title == '' or new_model.body == '':
            goofed['goofed'] = 1
            return {'entry': goofed}   # http exception here
        request.dbsession.add(new_model)
        return HTTPFound(request.route_url('home'))


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        data_from_DB = query.order_by(MyModel.title).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': data_from_DB}


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
