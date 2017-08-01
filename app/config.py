class BaseConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://rysxbcmtfrizgg:f83aa7c7c22300b62cd5cf475948efd146a33136c06b8029d44645a688e7d57c@ec2-184-73-236-170.compute-1.amazonaws.com/db7ai5ug00k7do'
    SECRET_KEY = "mysecretalone"


class TestConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/testingdb'


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
