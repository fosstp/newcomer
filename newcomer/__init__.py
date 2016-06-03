from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    # session settings
    from pyramid.settings import asbool
    if asbool(settings['production_mode']) is True:
        # using pyramid_redis_sessions
        config.include('pyramid_redis_sessions')
    else:
        # using builtin session mechanism
        from pyramid.session import SignedCookieSessionFactory
        sessions_secret = settings['sessions.secret']
        session_factory = SignedCookieSessionFactory(sessions_secret)
        config.set_session_factory(session_factory)

    # transaction manager settings, used by pyramid_sqlalchemy and
    # pyramid_mailer
    config.include('pyramid_tm')

    # database settings
    config.include('pyramid_sqlalchemy')

    # mailer settings
    #config.include('pyramid_mailer')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('signup_detail', '/signup_detail')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{id:\d+}')
    config.add_route('upload_via_enroll', '/upload/enroll')
    config.add_route('upload_via_schoolsoft', '/upload/schoolsoft')
    config.add_route('export_to_schoolsoft', '/export/schoolsoft')
    config.add_route('export_to_enroll', '/export/enroll')
    config.add_route('export_to_moe', '/export/moe')
    config.add_route('export_to_ecard', '/export/ecard')

    # i18n settings
    #config.add_translation_dirs('newcomer:locale')

    config.scan()
    return config.make_wsgi_app()
