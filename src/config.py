import os

class Config:
    """Base configuration for all environments."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG_TB_INTERCEPT_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # No need for SQLALCHEMY_DATABASE_URI here since it's in secret_keys.py

class ProductionConfig(Config):
    DEBUG = False
    # No need for SQLALCHEMY_DATABASE_URI here since it's in secret_keys.py

class TestingConfig(Config):
    TESTING = True
    # No need for SQLALCHEMY_DATABASE_URI here since it's in secret_keys.py

CURR_USER_KEY = 'user_id'
