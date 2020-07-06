import random
import string

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(20))

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/$USER/app/app/images/uploads"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    
    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/$USER/projects/flask_app/app/app/images/uploads"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/$USER/projects/flask_app/app/app/images/uploads"

    SESSION_COOKIE_SECURE = False