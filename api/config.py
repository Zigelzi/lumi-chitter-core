import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI") or f"sqlite:///{basedir}/dev.db"
    )
    DEBUG = True
