class BaseConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgres://gvbgebgkmbusei:e705e80ca127b5a0a5f4b107b49e2a2b3c45037d49514655b633694405a54bc0@ec2-107-20-250-195.compute-1.amazonaws.com:5432/d67pqgge6unh4g'
    SECRET_KEY = "mysecretalone"


class TestConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://gvbgebgkmbusei:e705e80ca127b5a0a5f4b107b49e2a2b3c45037d49514655b633694405a54bc0@ec2-107-20-250-195.compute-1.amazonaws.com:5432/d67pqgge6unh4g'

class DevelopmentConfig(BaseConfig):
    """Configurations for Development."""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Configurations for Production."""
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
}
