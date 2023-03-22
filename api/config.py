class Config(object):
    TESTING = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    DEBUG = True
