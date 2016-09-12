import requests
import os
import sys
import transaction
from ..views.default import ENTRIES_DATA

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


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


def main(argv=sys.argv):
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
        for entry in ENTRIES_DATA:
            row = MyModel(title=entry['title'], body=entry['body'], creation_date=entry['creation_date'])
            dbsession.add(row)

        resp = requests.get('https://sea401d4.crisewing.com/api/export?apikey=e31e0594-5513-4a37-8dd1-f8e49b68bfdb')
        info = resp.json()
        info = process_json(info)
        print(info)

        for retrieved_entry in info:
            query = dbsession.query(MyModel).filter(MyModel.title == retrieved_entry['title']).first()
            if len(query) == 0:
                row = MyModel(title=retrieved_entry['title'], body=retrieved_entry['body'], creation_date=retrieved_entry['creation_date'])
                dbsession.add(row)
        print('retrieved data added.')
