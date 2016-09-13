import datetime
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


def fix_date(curr_date):
    is_numerical_form = False
    try:
        int(curr_date[0])
        is_numerical_form = True
    except ValueError:
        return curr_date

    if is_numerical_form:
        new_date = datetime.date(int(curr_date[0:4]), int(curr_date[5:7]), int(curr_date[8:]))
        return new_date.strftime('%B %d, %Y')


def main(argv=sys.argv):
    if len(argv) < 2:
        sys.exit(1)
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
        # fix bogus entry
        query = dbsession.query(MyModel).filter(MyModel.title == 'You\'ve been H4x0r3d again!')
        if query is not None:
            try:
                query.delete()
                print('Bogus entry removed--hah')
            except DBAPIError:
                print('There was an error removing lame post.')

        # fix dates
        query = dbsession.query(MyModel).all()
        entries = []
        for row in query:
            if row in entries:
                break

            entries.append(row)
            try:
                curr_date = row.creation_date
                if len(curr_date) > 0:
                    row.creation_date = fix_date(curr_date)
            except DBAPIError:
                print('Error fixing dates.')


if __name__ == "__main__":
    main()
