
# OLD CODE
# """Flask app for dsm-diagnosis tool."""

# import os
# from flask import Flask, g, session
# from flask_migrate import Migrate
# from flask_wtf import CSRFProtect
# from flask_debugtoolbar import DebugToolbarExtension
# from src.application.models import (
#     db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis,
#     Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom
# )
# from src.application.secret_keys import SECRET_KEY, SQLALCHEMY_DATABASE_URI  # Import both vars from secret_keys.py
# from src.config import DevelopmentConfig, ProductionConfig, CURR_USER_KEY


# # Initialize the app
# app = Flask(__name__, static_folder='../application/static')

# # Load configuration based on environment
# env = os.environ.get('FLASK_ENV', 'development')
# if env == 'production':
#     app.config.from_object(ProductionConfig)
# else:
#     app.config.from_object(DevelopmentConfig)

# # Set the secret key and database URI from the secret_keys.py file
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# # Set UPLOAD_FOLDER for file uploads
# UPLOAD_FOLDER = os.path.join(app.root_path, '../application/static/uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure the uploads folder exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Initialize CSRF Protection
# csrf = CSRFProtect(app)

# # Initialize extensions
# debug = DebugToolbarExtension(app)
# connect_db(app)

# # Initialize Flask-Migrate
# migrate = Migrate(app, db)

# # Import and register Blueprints
# from src.application.blueprints.homepage.routes import homepage_bp
# from src.application.blueprints.user.routes import user_bp
# from src.application.blueprints.dsm.routes import dsm_bp
# from src.application.blueprints.psychopathology.routes import psychopathology_bp

# app.register_blueprint(homepage_bp)
# app.register_blueprint(user_bp)
# app.register_blueprint(dsm_bp)
# app.register_blueprint(psychopathology_bp)

# @app.before_request
# def add_user_to_g():
#     """Set g.user and g.logged_in before each request."""
#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])
#         g.logged_in = True
#     else:
#         g.user = None
#         g.logged_in = False




#  NEW CODE

"""Flask app for dsm-diagnosis tool."""

import os
from flask import Flask, g, session
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql import text  
from src.application.models import (
    db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis,
    Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom
)
from src.application.secret_keys import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from src.config import DevelopmentConfig, ProductionConfig, CURR_USER_KEY


def create_app(config_name='development'):
    """App factory to create a Flask app instance."""
    app = Flask(__name__, static_folder='../application/static')

    # Load configuration based on environment
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Set the secret key and database URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    # Set UPLOAD_FOLDER for file uploads
    UPLOAD_FOLDER = os.path.join(app.root_path, '../application/static/uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Initialize CSRF Protection
    csrf = CSRFProtect(app)

    # Initialize extensions
    debug = DebugToolbarExtension(app)
    connect_db(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import and register Blueprints
    from src.application.blueprints.homepage.routes import homepage_bp
    from src.application.blueprints.user.routes import user_bp
    from src.application.blueprints.dsm.routes import dsm_bp
    from src.application.blueprints.psychopathology.routes import psychopathology_bp

    app.register_blueprint(homepage_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dsm_bp)
    app.register_blueprint(psychopathology_bp)

    @app.before_request
    def add_user_to_g():
        """Set g.user and g.logged_in before each request."""
        if CURR_USER_KEY in session:
            g.user = User.query.get(session[CURR_USER_KEY])
            g.logged_in = True
        else:
            g.user = None
            g.logged_in = False

    return app


# # For development runs directly (optional)
# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)

# Create app instance for Gunicorn
app = create_app()
