import os

class Config:
    """Base configuration for all environments."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False  # Disable SQLAlchemy echo in production

class TestingConfig(Config):
    TESTING = True

CURR_USER_KEY = 'user_id'
