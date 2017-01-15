import pytest
import transaction

from pyramid import testing

from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base
from learning_journal.scripts.initializedb import ENTRIES
import os


TEST_DB = 'postgres://maellevance:password@localhost:5432/LJ_test_db'

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
    settings = {
        'sqlalchemy.url': TEST_DB
    }
    config = testing.setUp(settings=settings)
    config.include("learning_journal.models")
    config.testing_securitypolicy(userid='maelle', permissive=True)

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session."""
    return testing.DummyRequest(dbsession=db_session)


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


@pytest.fixture
def set_auth_credentials():
    """Make a username/password combo for testing."""
    from passlib.apps import custom_app_context as pwd_context

    os.environ["AUTH_USERNAME"] = "testme"
    os.environ["AUTH_PASSWORD"] = pwd_context.hash("foobar")

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


def test_api_returns_json(dummy_request, db_session, adding_models):
    """Test api view returns a json object."""
    from learning_journal.views.default import api_list_view
    result = api_list_view(dummy_request)
    assert isinstance(result, object)

def test_check_credentials_wrong_password(set_auth_credentials):
    """Test check credential will return false with wrong password."""
    from learning_journal.security import check_credentials
    assert not check_credentials('hello', 'wrong password')

# ======== FUNCTIONAL TESTS ===========


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{'sqlalchemy.url': TEST_DB})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    return testapp


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


@pytest.fixture
def login_fixture(testapp, set_auth_credentials):
    """Test that logging redirects."""
    resp = testapp.post('/login', params={'username': 'testme', 'password': 'foobar'})
    headers = resp.headers
    return headers


def test_home_route_has_ul(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("ul")) == 1


def test_create_view_has_form(testapp, login_fixture):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/new-entry', login_fixture)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_edit_view_has_form(testapp, fill_the_db, login_fixture):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/1/edit-entry', login_fixture)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_edit_view_has_entry(testapp, fill_the_db, login_fixture):
    """Test that the edit view has a form on it."""
    response = testapp.get('/journal/1/edit-entry', login_fixture)
    body = response.html.find_all(class_='text_area')[0].getText()
    assert ENTRIES[0]["body"] in body


def test_detail_route_loads_correct_entry(testapp, fill_the_db):
    """Test that the detail route loads the correct entry."""
    response = testapp.get('/journal/2')
    title = response.html.find_all(class_='post_title')[0].getText()
    body = response.html.find_all(class_='post_body')[0].getText()
    assert title == ENTRIES[1]["title"]
    assert body == ENTRIES[1]["body"]


def test_404_returns_notfound_template(testapp):
    """Test that a wrong url will render the 404 template."""
    response = testapp.get('/journal/500', status=404)
    title = response.html.find_all(class_='not_found')[0].getText()
    assert "404 Page not found" in title


def test_login_update_ok(testapp, set_auth_credentials):
    """Test that logging redirects."""
    resp = testapp.post('/login', params={'username': 'testme', 'password': 'foobar'})
    assert resp.status_code == 302


def test_new_entry_logged_in_authorized(testapp, login_fixture):
    """Test that new-entry page is accessible when logged in."""
    resp = testapp.get('/journal/new-entry', login_fixture)
    assert resp.status_code == 200


def test_login_page_has_form(testapp):
    """Test that the login route brings up the login template."""
    html = testapp.get('/login').html
    assert len(html.find_all('input'))


def test_new_entry_not_logged_in(testapp):
    """Test new-entry route without logging in makes 403 error."""
    from webtest.app import AppError
    with pytest.raises(AppError):
        testapp.get('/journal/new-entry')


def test_edit_entry_not_logged_in(testapp):
    """Test edit-entry route without logging in makes 403 error."""
    from webtest.app import AppError
    with pytest.raises(AppError):
        testapp.get('/journal/1/edit-entry')


def test_edit_entry_logged_in_authorized(testapp, login_fixture, fill_the_db):
    """Test edit-entry route is accessible when logged-in."""
    resp = testapp.get('/journal/1/edit-entry', login_fixture)
    assert resp.status_code == 200


def test_logout_redirects(testapp):
    """Test logout view redirects."""
    resp = testapp.get('/logout')
    assert resp.status_code == 302


def test_logout_redirect_to_home(testapp):
    """Test logout view redirects to home view."""
    resp = testapp.get('/logout')
    full_resp = resp.follow()
    assert len(full_resp.html.find_all('ul')) == 1


def test_update_authorized_wrong_url_raises_404(testapp, login_fixture):
    """Test update view with wrong entry will raise 404 if authorized."""
    from webtest.app import AppError
    with pytest.raises(AppError, message="Bad response: 404 Not Found"):
        testapp.get('/journal/1/edit-entry', login_fixture)


def test_delete_authorized_deletes(testapp, login_fixture, fill_the_db):
    """Test after delete route is hit, index view doesn't have the entry."""
    resp = testapp.get('/2/delete', login_fixture)
    full_resp = resp.follow()
    index_page_entries = full_resp.html.find_all('ul')[0].getText()
    assert "Day 13" not in index_page_entries
    assert "Day 12" in index_page_entries


def test_delete_authorized_redirects(testapp, login_fixture, fill_the_db):
    """Test delete route redirects."""
    resp = testapp.get('/2/delete', login_fixture)
    assert resp.status_code == 302
