def includeme(config):
    config.add_static_view('static', 'website:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/journal/1')
    config.add_route('edit', '/journal/1/edit-entry')
    config.add_route('new', '/journal/new-entry')
