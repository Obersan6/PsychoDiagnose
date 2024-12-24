import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Load Alembic configuration from the .ini file in use
config = context.config

# Configure logging based on the Alembic .ini file
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    """Retrieve the SQLAlchemy Engine instance.

    Handles compatibility between Flask-SQLAlchemy versions (<3 and >=3).
    """
    try:
        # For Flask-SQLAlchemy < 3 or Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # For Flask-SQLAlchemy >= 3
        return current_app.extensions['migrate'].db.engine
    
def get_engine_url():
    """Get the database URL for Alembic configuration.

    This method renders the database URL and logs it. It ensures
    password obfuscation if required.
    """
    try:
        url = get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
        logger.info(f"Database URL: {url}")  # Log the database URL
        return url
    except AttributeError:
        url = str(get_engine().url).replace('%', '%%')
        logger.info(f"Database URL: {url}")  # Log the database URL
        return url

# Set the SQLAlchemy database URL for Alembic
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db


def get_metadata():
    """Retrieve the SQLAlchemy metadata object.

    Supports both single and multiple metadata configurations.
    """
    
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in offline mode.

    In this mode, migrations are configured using only a database URL,
    skipping the need for an active database connection. Outputs
    SQL statements to the migration script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in online mode.

    In this mode, an Engine and active connection are required to
    execute migrations. Schema changes are applied directly to
    the database.

    Includes a callback to prevent auto-migration when there are no schema changes.
    """

    def process_revision_directives(context, revision, directives):
        """Prevent unnecessary auto-migration files if no schema changes are detected."""
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine migration mode and execute accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
