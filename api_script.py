import requests
import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from website.models.meta import Base
from website.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from website.models import MyModel
from sqlalchemy.exc import DBAPIError


def format_date(date):
    """Truncate date format."""
    return date[0:10]


def process_json(info):
    ret_list = []
    title_list = []
    for entry in info:
        e = {}
        e['title'] = entry['title']
        e['creation_date'] = format_date(entry['created'])
        e['body'] = entry['text']
        if e['title'] not in title_list:
            ret_list.append(e)
            title_list.append(e['title'])
    return ret_list


def import_entries(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        #for entry in ENTRIES_DATA:
        #    query = dbsession.query(MyModel).filter(MyModel.title == entry['title']).first()
        #    if len(query) == 0:
        #        row = MyModel(title=entry['title'], body=entry['body'], creation_date=entry['creation_date'])
        #        dbsession.add(row)

    try:
        resp = requests.get('https://sea401d4.crisewing.com/api/export?apikey=e31e0594-5513-4a37-8dd1-f8e49b68bfdb')
        info = resp.json()
        info = process_json(info)
        print(info)
    except:
        print('There was an error requesting the data.')
        sys.exit(1)

    for retrieved_entry in info:
        query = dbsession.query(MyModel).filter(MyModel.title == retrieved_entry['title']).first()
        if len(query) == 0:
            try:
                row = MyModel(title=retrieved_entry['title'], body=retrieved_entry['body'], creation_date=retrieved_entry['creation_date'])
                dbsession.add(row)
            except DBAPIError:
                print('There was an error.')
                break
    print('retrieved data added.')