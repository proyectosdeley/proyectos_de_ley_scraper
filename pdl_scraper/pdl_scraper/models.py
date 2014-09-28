import dataset


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    database = [
        settings.DATABASE['drivername'],
        '//' + settings.DATABASE['username'],
        settings.DATABASE['password'] + '@' + settings.DATABASE['host'],
        settings.DATABASE['port'] + '/' + settings.DATABASE['database'],
    ]
    url = ':'.join(database)
    db = dataset.connect(url)
    return db
