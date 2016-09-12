import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow
from pyramid.security import Everyone, Authenticated
from passlib.apps import custom_app_context as pwd_context


class RootAccess(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'root')
    ]


def verify_user(username, password):
    authenticated = False
    env_username = os.environ.get('AUTH_USER_LJ', '')
    env_password = os.environ.get('AUTH_PASS_LJ', '')
    print('env user/pass', env_username, env_password)
    if env_username and env_password:
        if username == env_username:
            try:
                authenticated = pwd_context.verify(password, env_password)
            except ValueError:
                print('ValueError in verify_user')
    print(authenticated)
    return authenticated


def includeme(config):
    """security-related configuration"""
    os.environ['AUTH_PASS_LJ'] = pwd_context.encrypt('goober')
    auth_secret = os.environ.get('AUTH_SECRET_LJ', '')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )

    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(RootAccess)
