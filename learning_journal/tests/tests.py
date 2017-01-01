import pytest
import transaction

from pyramid import testing

from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base
from learning_journal.scripts.initializedb import ENTRIES
import time


MODEL_ENTRIES = [Entry(
    title=entry['title'],
    body=entry['body'],
    creation_date=entry['creation_date']
) for entry in ENTRIES]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://maellevance:password@localhost:5432/LJ_test_db'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config

@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session, method="GET"):
    """Instantiate a fake HTTP Request, complete with a database session."""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = db_session
    return request


@pytest.fixture
def adding_models(dummy_request):
    """Add models to the database."""
    for entry in ENTRIES:
        row = Entry(
            title=entry['title'],
            body=entry['body'],
            creation_date=entry['creation_date']
        )

        dummy_request.dbsession.add(row)


# =====Unit Test====

def test_home_list_returns_empty_when_empty(dummy_request):
    """Test that the home list returns no objects in the expenses iterable."""
    from learning_journal.views.default import home_list
    result = home_list(dummy_request)
    query_list = result["posts"][:]
    assert len(query_list) == 0


def test_new_entries_are_added(db_session):
    """New entries get added to the database."""
    db_session.add_all(MODEL_ENTRIES)
    query = db_session.query(Entry).all()
    assert len(query) == len(MODEL_ENTRIES)


def test_home_list_returns_objects_when_exist(dummy_request, db_session):
    """Test that the home list does return objects when the DB is populated."""
    from learning_journal.views.default import home_list
    model = Entry(title=ENTRIES[0]["title"],
                  body=ENTRIES[0]["body"],
                  creation_date=ENTRIES[0]["creation_date"])
    db_session.add(model)
    result = home_list(dummy_request)
    query_list = result["posts"][:]
    assert len(query_list) == 1


def test_create_new_entry_creates_new(db_session, dummy_request):
    """Test when new entry is create the db is updated."""
    from learning_journal.views.default import create

    dummy_request.method = "POST"
    dummy_request.POST["title"] = "Some Title"
    dummy_request.POST["body"] = "So informational. Much learning."

    with pytest.raises(Exception):
        create(dummy_request)

    query = db_session.query(Entry).all()
    assert query[0].title == "Some Title"
    assert query[0].body == "So informational. Much learning."


def test_detail_returns_entry_1(dummy_request, db_session):
    """Test that entry return entry one."""
    from learning_journal.views.default import detail
    model = Entry(title=ENTRIES[0]["title"],
                  body=ENTRIES[0]["body"],
                  creation_date=ENTRIES[0]["creation_date"],
                  id=ENTRIES[0]["id"])
    db_session.add(model)
    dummy_request.matchdict['id'] = 1
    result = detail(dummy_request)
    query_result = result["post"]
    assert query_result.title == ENTRIES[0]["title"]
    assert query_result.body == ENTRIES[0]["body"]



@pytest.fixture
def testapp():
    """Create an instance of our app for testing."""
    from webtest import TestApp
    from learning_journal import main
    app = main({})
    return TestApp(app)


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances.
    Start a database session with the transaction manager and add all of the
    expenses. This will be done anew for every test.
    """
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        for entry in ENTRIES:
            row = Entry(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dbsession.add(row)


def test_home_route_has_ul(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("ul")) == 1


def test_create_view_has_form(testapp):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_edit_view_has_form(testapp):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/1/edit-entry', status=200)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_edit_view_has_entry(testapp):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/1/edit-entry', status=200)
    body = response.html.find_all(class_='text_area')[0].getText()
    assert ENTRIES[0]["body"] in body


def test_detail_route_loads_correct_entry(testapp, fill_the_db):
    """Test that the detail route loads the correct entry."""
    response = testapp.get('/journal/2', status=200)
    title = response.html.find_all(class_='post_title')[0].getText()
    body = response.html.find_all(class_='post_body')[0].getText()
    assert title == ENTRIES[1]["title"]
    assert body == ENTRIES[1]["body"]