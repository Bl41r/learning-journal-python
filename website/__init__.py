from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if 'sqlalchemy.url' not in settings:
        settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'website:static', cache_max_age=3600)
    config.include('.security')
    config.include('.routes')
    config.include('.models')
    config.scan()

    return config.make_wsgi_app()
