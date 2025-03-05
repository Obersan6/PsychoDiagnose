
import secrets

# Generate a 32-byte SECRET_KEY
SECRET_KEY = secrets.token_hex(32)

# Define my SQLALCHEMY_DATABASE_URI for development
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Caccolino5@localhost/diagnosis_db'

# Define my SQLALCHEMY_DATABASE_URI for deployment
SQLALCHEMY_DATABASE_URI = "postgresql://postgres.rdsnxgihfwemtrdynqol:5SerHappySubitoGia7@aws-0-eu-west-2.pooler.supabase.com:6543/postgres"


