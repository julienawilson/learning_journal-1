"""Views for pyramid learning journal server."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import exception_response
import time
from sqlalchemy.exc import DBAPIError
from learning_journal.security import check_credentials
from pyramid.security import remember, forget

from ..models import Entry


@view_config(route_name="home", renderer="../templates/index.jinja2")
def home_list(request):
    """View for the home page."""
    try:
        query = request.dbsession.query(Entry)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'posts': query}


@view_config(route_name="detail", renderer="../templates/post_details.jinja2")
def detail(request):
    """View for the detail page."""
    query = request.dbsession.query(Entry)
    post_dict = query.filter(Entry.id == request.matchdict['id']).first()
    if post_dict is not None:
        return {"post": post_dict}
    raise exception_response(404)


@view_config(
    route_name="create",
    renderer="../templates/new_post_form.jinja2",
    permission="add")
def create(request):
    """View for create page."""
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST["body"]
        creation_date = time.strftime("%m/%d/%Y")
        new_model = Entry(title=title, body=body, creation_date=creation_date)
        request.dbsession.add(new_model)
        return HTTPFound(location=request.route_url('home'))
    return {}


@view_config(
    route_name="update",
    renderer="../templates/edit_post_form.jinja2",
    permission="add")
def update(request):
    """View for update page."""
    if request.method == "POST":
        try:
            """If we submit the form, it will update the entry in DB."""
            title = request.POST['title']
            body = request.POST["body"]
            creation_date = time.strftime("%m/%d/%Y")
            query = request.dbsession.query(Entry)
            post_dict = query.filter(Entry.id == request.matchdict['id'])
            post_dict.update({"title": title, "body": body, "creation_date": creation_date})
            return HTTPFound(location='/')
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
    query = request.dbsession.query(Entry)
    post_dict = query.filter(Entry.id == request.matchdict['id']).first()
    if post_dict is not None:
        a = {
            'title': post_dict.title,
            'creation_date': post_dict.creation_date,
            'body': post_dict.body}
        return {"post": a}
    raise exception_response(404)


@view_config(
    route_name="login",
    renderer="../templates/login.jinja2",
    require_csrf=False)
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                location=request.route_url("home"),
                headers=auth_head
            )

    return {}


@view_config(route_name="logout")
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(location=request.route_url("home"), headers=auth_head)


@view_config(route_name="delete", permission="delete")
def delete_view(request):
    """To delete individual entry."""
    entry = request.dbsession.query(Entry).get(request.matchdict["id"])
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url("home"))


@view_config(route_name="api_list", renderer="string")
def api_list_view(request):
    entries = request.dbsession.query(Entry).all()
    output = [entry.to_json() for entry in entries]
    return output



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
