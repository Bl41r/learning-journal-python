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
        'body': 'Today, we learned about templating with Jinja, and about the binary tree data type.  I spent most of the time revising old data structures, since it is not a good idea to coninue building upon something that is not perfect.  I also got my journal site deployed with the templates working.  Lastly, we formed project groups, and I will be working on my idea for a market analysis web application.'},
    {
        'title': 'Day14',
        'creation_date': 'August 25, 2016',
        'body': "Today, we learned about using postgres for our databases. I'm still a bit confused over the sheer amount of information of the past few days. We also learned about graphs and started implementing one today."
    },
    {
        'title': 'Day13',
        'creation_date': 'August 24, 2016',
        'body': 'Blah Blah Blah Python is hard... also, we learned about using SQLAlchemy, the priority queue. I also gave my lightning talk on the Collatz conjecture.'
    },
    {
        'title': 'Day9',
        'creation_date': 'August 20, 2016',
        'body': "Today, we learned about properties in python, which seem very useful for classes which have related attributes that must be changed when another one is updated, as well as for when you want to make some attributes be read-only. We also got some helpful pointers on my code review, which was not pretty :). We built a Queue data structure, and worked on our http server."
    },
    {
        'title': 'Day10',
        'creation_date': 'August 18, 2016',
        'body': "Today, I we began with a gist assignment involving substrings of a maximum length. I believe that I did relatively well on it. We then had a whiteboard challenge to create al algorithm to create a function to determine if a given node has an upstream node which causes a loop in the entire list of nodes. Afterwards, we worked on our weekly data structure and http server assignments."
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
    data = query.filter_by(id=request.matchdict['id']).one()
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
        data2['body'] = request.POST['body']
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
        data_from_DB = query.all()
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
