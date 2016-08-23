from pyramid.config import Configurator


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('edit', '/journal/edit-entry')
    config.include('.routes')
    config.include('.views')
    config.scan()
    return config.make_wsgi_app()
