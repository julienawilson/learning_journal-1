"""Views for pyramid learning journal server."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import time
from sqlalchemy.exc import DBAPIError

from ..models import Entry

# @view_config(route_name="create", renderer="../templates/form.jinja2")
# def create_view(request):
#     import pdb;pdb.set_trace()
#     if request.method == "POST":
#         #get the form stuff
#         return {}
#     return {}


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
    return {"post": post_dict}


@view_config(route_name="create", renderer="../templates/new_post_form.jinja2")
def create(request):
    """View for create page."""
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST["body"]
        creation_date = time.strftime("%m/%d/%Y")
        new_model = Entry(title=title, body=body, creation_date=creation_date)
        request.dbsession.add(new_model)
        return HTTPFound(location='/')
    return {}


@view_config(route_name="update", renderer="../templates/edit_post_form.jinja2")
def update(request):
    """View for update page."""
    if request.method == "POST":
        try:
            title = request.POST.get('title')
            body = request.POST["body"]
            creation_date = time.strftime("%m/%d/%Y")
            new_model = Entry(title=title, body=body, creation_date=creation_date)
            request.dbsession.add(new_model)
            return HTTPFound(location='/')
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
    query = request.dbsession.query(Entry)
    post_dict = query.filter(Entry.id == request.matchdict['id']).first()
    a = {'title': post_dict.title,
         'creation_date': post_dict.creation_date,
         'body': post_dict.body}
    return {"post": a}


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
