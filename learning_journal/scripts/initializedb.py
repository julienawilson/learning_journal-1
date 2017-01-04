import os
import sys
import transaction

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
from ..models import Entry

ENTRIES = [
    {
        "title": "Day 12",
        "id": 1,
        "creation_date": "12/20/2016",
        "body": """Today I learned to make this.
          This is pretty awesome.
          I also learned to implement a Deque with Python. It was interesting to change partners this week as I get to know people I have never worked with. I think it went pretty well and even though I'm leaving later than expected I did learn a ton and the work was equally divided.
          I'm also getting feedback on our server assignment and so far I'm pretty happy with that.
          Looking forward to use Jinja2 and templating a bit more so writing this learning journal won't be as tedious anymore.
          I'm also excited to pitch my idea to the class tomorrow and really hope I will be able to convey how important for people with apraxia and other disabilities it could be.
          """
    },
    {
        "title": "Day 13",
        "id": 2,
        "creation_date": "12/21/16",
        "body": """Today I learned that I don't know how to implement a Deque.
          So there's that.
          Jinja2 templating is really similar to Django templates which have a (very minimal) experience with so it wasn't too overwhelming.
          I'm excited to implement a database so I don't have to harcode this.
        """
    },
]


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):  # pragma: no cover
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
        for post in ENTRIES:
            model = Entry(title=post["title"], body=post["body"], creation_date=post["creation_date"])
            dbsession.add(model)
