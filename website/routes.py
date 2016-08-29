def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', r'/')
    #config.add_route('home_orig', r'/home')
    config.add_route('detail', r'/journal/{id:\d+}')
    config.add_route('edit', r'/journal/{id:\d+}/edit-entry')
    config.add_route('new', r'/journal/new-entry')
