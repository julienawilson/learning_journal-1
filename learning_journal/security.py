import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
# ACL = Acces Control List
from pyramid.security import Allow, Authenticated
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import SignedCookieSessionFactory


class NewRoot(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'add')
    ]


def check_credentials(username, password):
    """Return True if correct username and password, else False."""
    if username and password:
        # proceed to check credentials
        if username == os.environ["AUTH_USERNAME"]:
            return pwd_context.verify(password, os.environ["AUTH_PASSWORD"])
    return False


def includeme(config):
    """Pyramid security configuration."""
    auth_secret = os.environ.get("AUTH_SECRET", "secret")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    # config.set_default_permission("view")
    config.set_root_factory(NewRoot)
    session_secret = os.environ.get('SESSION_SECRET', 'secret')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
