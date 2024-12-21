"""Flask app for dsm-diagnosis tool."""

import os
from flask import Flask, g, session
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from src.application.models import (
    db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis,
    Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom
)
from src.application.secret_keys import SECRET_KEY, SQLALCHEMY_DATABASE_URI  # Import both vars from secret_keys.py
from src.config import DevelopmentConfig, ProductionConfig, CURR_USER_KEY

# Initialize the app
app = Flask(__name__, static_folder='../application/static')

# Load configuration based on environment
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Set the secret key and database URI from the secret_keys.py file
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Set UPLOAD_FOLDER for file uploads
UPLOAD_FOLDER = os.path.join(app.root_path, '../application/static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
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


#####################################################################

# import os
# from flask import Flask, g, session
# from flask_migrate import Migrate
# from flask_wtf import CSRFProtect
# from flask_debugtoolbar import DebugToolbarExtension
# from src.application.models import db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis, Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom
# from src.application.secret_keys import SECRET_KEY, SQLALCHEMY_DATABASE_URI
# from src.config import DevelopmentConfig, ProductionConfig, TestingConfig, CURR_USER_KEY

# # THIS IS THE PREVIOUS CONFIGURATION DURING TESTING
# def create_app(config_class=None):
#     """Factory to create a Flask application."""
#     app = Flask(__name__, static_folder='../application/static')

#     # Set the configuration
#     config_class = config_class or DevelopmentConfig
#     app.config.from_object(config_class)

#     # Set the secret key and database URI
#     app.config['SECRET_KEY'] = SECRET_KEY
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

#     # Configure Flask Debug Toolbar to not intercept redirects
#     app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False  # Add this line here


#     # Set UPLOAD_FOLDER for file uploads
#     UPLOAD_FOLDER = os.path.join(app.root_path, '../application/static/uploads')
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#     # Ensure the uploads folder exists
#     try:
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.makedirs(UPLOAD_FOLDER)
#     except OSError as e:
#         app.logger.error(f"Failed to create upload folder: {e}")

#     # Initialize extensions
#     csrf = CSRFProtect(app)
#     DebugToolbarExtension(app)
#     connect_db(app)
#     Migrate(app, db)

#     # Import and register blueprints
#     from src.application.blueprints.homepage.routes import homepage_bp
#     from src.application.blueprints.user.routes import user_bp
#     from src.application.blueprints.dsm.routes import dsm_bp
#     from src.application.blueprints.psychopathology.routes import psychopathology_bp

#     app.register_blueprint(homepage_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(dsm_bp)
#     app.register_blueprint(psychopathology_bp)

#     @app.before_request
#     def add_user_to_g():
#         """Set g.user and g.logged_in before each request."""
#         if CURR_USER_KEY in session:
#             g.user = User.query.get(session[CURR_USER_KEY])
#             g.logged_in = True
#         else:
#             g.user = None
#             g.logged_in = False

#     return app


# # Flask run entry point
# app = create_app()  # Default to development config

# import os
# from flask import Flask, g, session
# from flask_migrate import Migrate
# from flask_wtf import CSRFProtect
# from flask_debugtoolbar import DebugToolbarExtension
# from src.application.models import (
#     db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis,
#     Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom
# )
# from src.config import DevelopmentConfig, CURR_USER_KEY

# def create_app(config_class=None):
#     """Factory to create a Flask application."""
#     app = Flask(__name__, static_folder='../application/static')

#     # Set the configuration
#     config_class = config_class or DevelopmentConfig
#     app.config.from_object(config_class)

#     # Configure Flask Debug Toolbar to not intercept redirects
#     app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

#     # Set UPLOAD_FOLDER for file uploads
#     UPLOAD_FOLDER = os.path.join(app.root_path, '../application/static/uploads')
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#     # Ensure the uploads folder exists
#     try:
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.makedirs(UPLOAD_FOLDER)
#     except OSError as e:
#         app.logger.error(f"Failed to create upload folder: {e}")

#     # Initialize extensions
#     csrf = CSRFProtect(app)
#     DebugToolbarExtension(app)
#     connect_db(app)
#     Migrate(app, db)

#     # Import and register blueprints
#     from src.application.blueprints.homepage.routes import homepage_bp
#     from src.application.blueprints.user.routes import user_bp
#     from src.application.blueprints.dsm.routes import dsm_bp
#     from src.application.blueprints.psychopathology.routes import psychopathology_bp

#     app.register_blueprint(homepage_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(dsm_bp)
#     app.register_blueprint(psychopathology_bp)

#     @app.before_request
#     def add_user_to_g():
#         """Set g.user and g.logged_in before each request."""
#         if CURR_USER_KEY in session:
#             g.user = User.query.get(session[CURR_USER_KEY])
#             g.logged_in = True
#         else:
#             g.user = None
#             g.logged_in = False

#     return app

# # Create the Flask app instance
# app = create_app()





# Initialize the app
# app = Flask(__name__)
# Commented out for testing
# app = Flask(__name__, static_folder='../application/static') 
# app = create_app()

# # Load configuration based on environment
# env = os.environ.get('FLASK_ENV', 'development')
# if env == 'production':
#     app.config.from_object(ProductionConfig)
# else:
#     app.config.from_object(DevelopmentConfig)














# # Initialize LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'user.signin'  # Redirect to the 'signin' route in user_bp for login

# # Define the user loader function
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# Create database tables (if needed)
# with app.app_context():
#     db.create_all()


























